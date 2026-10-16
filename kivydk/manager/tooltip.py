#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 18 Sep 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
TooltipManager tracks pointer movement inside the window and determines
whether the cursor is hovering a widget that declares tooltip behavior.
When a tooltip-eligible widget is found, the manager selects the correct
tooltip widget (custom or default), updates its content, positions it and
controls its visibility. Only one tooltip is active at a time.
"""
__all__ = ("TooltipManager",)

#// IMPORT
from typing import cast

from kivy.animation import Animation
from kivy.clock import (
    Clock,
    ClockEvent,
)
from kivy.event import EventDispatcher
from kivy.eventmanager import EventManagerBase
from kivy.input.motionevent import MotionEvent
from kivy.properties import (
    BooleanProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    VariableListProperty,
)
from kivy.uix.widget import Widget
from kivy.vector import Vector

from kivydk.uix.abc.tooltip import TooltipTemplate
from kivydk.uix.tooltip import Tooltip
from kivydk.utils.numeric import clamp

# [ Debug ]
from kivy.graphics import Color, Ellipse, Rectangle


#// LOGIC
class TooltipManager(EventManagerBase, EventDispatcher):
    """
    Manages detection, creation, reuse, and visibility of tooltip widgets.

    The manager alternates between two modes:
        - **Idle mode** → a periodic timer checks for tooltip‑eligible widgets.
        - **Active mode** → tooltip position and content are updated immediately
          while the cursor remains over the hovered widget.
    """

    tooltip_template: ObjectProperty = ObjectProperty(Tooltip)
    """ Default tooltip widget class or instance used when no custom tooltip is provided. """

    tooltip_side: OptionProperty = OptionProperty(
        defaultvalue = "auto",
        options = ["auto", "cursor", "left", "top", "right", "bottom"]
    )
    """ Default preferred placement side for positioning the tooltip relative to the hovered widget. """

    tooltip_interactive: BooleanProperty = BooleanProperty(False)
    """ Default interactive mode applied when TooltipBehavior does not override it. """

    tooltip_offset: NumericProperty = NumericProperty(0)
    """ Default offset between the tooltip and the hovered widget. """

    edge_offset: VariableListProperty = VariableListProperty(0)
    """
    Minimum distance between the tooltip and the window edges.
    
    § variable list use ¶
    """

    idle_time: NumericProperty = NumericProperty(0.5)
    """
    Interval ``(in seconds)`` between deep‑search scans for tooltip‑enabled widgets.
    
    The manager checks the hovered widget tree periodically instead of on
    every mouse movement. If the cursor has not moved since the previous
    scan, the deep search is skipped to avoid unnecessary work.
    """

    delay_time: NumericProperty = NumericProperty(1.0)
    """
    Delay ``(in seconds)`` before showing a tooltip after a valid hovered widget
    is detected. This ensures the tooltip appears only when the user is
    intentionally hovering over the widget, not just passing over it.
    """

    animation_time: NumericProperty = NumericProperty(0.16)
    """
    Duration ``(in seconds)`` of the tooltip fade‑in and fade‑out animations.
    
    § sweet spot : 0.12, 0.18 ¶
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # The MotionEvent types this manager processes
        self.type_ids = ("touch", "hover")

        # Private variables
        self.__MOVE_THRESHOLD: float = 21.0
        self.__SIDE_MAX_WIDTH: str = "max width"
        self.__SIDE_MAX_HEIGHT: str = "max height"
        self.__SIDE_FALLBACK: str = "fallback"
        self.__SIDE_FALLBACK_ZERO: str = "fallback zero"
        self.__AXIS_MAP: dict[str, tuple[str, str]] = {
            "top": ("left", "right"),
            "left": ("top", "bottom"),
        }

        self.__hovered_widget: Widget | None = None
        self.__tooltip_widget: TooltipTemplate|None = None
        self.__next_tooltip_widget: TooltipTemplate|None = None

        self.__is_custom_tooltip: bool = False
        self.__is_tooltip_from_class: bool = False
        self.__is_tooltip_interactive: bool = False
        self.__event_canceled: bool = False

        self.__last_tooltip_side: str = ""
        self.__tooltip_distance: float = 0.0
        self.__last_pointer: Vector = Vector(-1.0, -1.0)

        self.__idle_timer: ClockEvent = Clock.create_trigger(self._cb_search_tooltip, self.idle_time, True)
        self.__show_timer: ClockEvent = Clock.create_trigger(self._cb_show_tooltip, self.delay_time, False)
        self.__animation = Animation(duration=self.animation_time, transition="linear")

    def stop(self) -> None:
        """ Deactivate the manager, reset internal references and cancel the clock tasks. """
        self.__on_leave_window()

        if self.__tooltip_widget:
            self.window.remove_widget(self.__tooltip_widget)

        self.__tooltip_widget = None
        self.__next_tooltip_widget = None

    # noinspection SpellCheckingInspection
    def dispatch(self, etype: str, me: MotionEvent) -> bool:
        """
        Process a MotionEvent and update the manager's state accordingly.

        § parameters : etype = One of ``"begin"``/, ``"update"`` or ``"end"`` ¶
        § param : me = The MotionEvent currently being dispatched ¶
        """
        if me.type_id == "hover" and not self.__event_canceled:
            # [ Idle mode ] When the cursor enters the window
            if etype == "begin":
                self.__idle_timer()

            elif etype == "update":
                # [ Active mode ] When interested widget is hovered
                if self.__hovered_widget:
                    if not self.__hovered_widget.collide_point(*self.window.mouse_pos):
                        if not self.__is_tooltip_interactive_or_near:
                            self.__make_tooltip_visible(False)
                            self.__hovered_widget = None

                # [ Idle mode ] When no interested widget is hovered
                elif not self.__idle_timer.is_triggered:
                    self.__idle_timer()

            # [ Stop ] When the cursor leaves the window
            elif etype == "end":
                self.__on_leave_window()

        else:
            # [ Stop ] When a mouse button is pressed or when an equivalent device action is triggered
            if etype == "begin":
                # [ Stop ] When the tooltip is not interactive or when the mouse cursor is outside the tooltip
                if not self.__is_tooltip_interactive_or_near:
                    self.__make_tooltip_visible(False)
                    self.__event_canceled = True

            # [ Idle mode ] When a mouse button is released or when an equivalent device action is triggered
            elif etype == "end":
                self.__event_canceled = False

        return False

    # noinspection PyUnusedParameter
    def _cb_search_tooltip(self, dt: float) -> None:
        """
        Callback what perform a tooltip lookup based on the current pointer position.

        This method it updates internal state and may trigger tooltip creation,
        reuse, or removal depending on the result of the search.
        """
        this_pos: list[float] = [*self.window.mouse_pos]

        # Skip deep search if the pointer was not moved
        if this_pos == self.__last_pointer:
            return None

        # Save a reference of the pointer for the next check
        self.__last_pointer.x, self.__last_pointer.y = this_pos

        # Locate the deepest interested widget
        found_widget: Widget|None = None
        for window_child in self.window.children:
            found_widget = self.__deep_search_widget(window_child, "kdk_tooltip", *this_pos)

            if found_widget:
                break

        # Skip if the found widget is the same as the last time
        if found_widget == self.__hovered_widget:
            return None

        # Save a reference of the last deep search and handle the tooltip logic base on that
        self.__hovered_widget = found_widget
        self.__resolve_tooltip_widget()

        return None

    # noinspection PyUnusedParameter
    def _cb_show_tooltip(self, dt: float) -> None:
        """ Callback used to show the tooltip. """
        self.__update_tooltip_position()

        if self.__hovered_widget:
            # Hide on large pointer movement, but always update tooltip references
            still_show: bool = self.__last_pointer.distance(self.window.mouse_pos) < self.__MOVE_THRESHOLD
            self.__make_tooltip_visible(still_show)

    def __deep_check_tooltip_side(
            self, wanted: str, mirror: bool = True, cross: bool = True, cross_mirror: bool = True
    ) -> str:
        """
        Validate the requested tooltip side and resolve a fallback if needed.

        The method checks whether the tooltip fits on the requested side.
        If not, it tries the mirrored side (*left* ↔ *right*, *top* ↔ *bottom*) and then
        the cross‑axis sides (*horizontal* ↔ *vertical*) depending on the fallback flags.
        """
        tooltip: TooltipTemplate|None = self.__next_tooltip_widget or self.__tooltip_widget

        if tooltip is None:
            return self.__SIDE_FALLBACK_ZERO

        # Direct fit check
        match wanted:
            # Pick the side with the most available space
            case "auto":
                biggest_side: str = max(("left", "top", "right", "bottom"), key=lambda s: self.__get_side_size(s))
                checked_side: str = self.__deep_check_tooltip_side(biggest_side, False, False)
                return "cursor" if (checked_side == self.__SIDE_FALLBACK) else checked_side

            case "left" | "right":
                if tooltip.width <= self.__get_side_size(wanted):
                    return wanted

            case "top" | "bottom":
                if tooltip.height <= self.__get_side_size(wanted):
                    return wanted

            case "cursor":
                return wanted

            # Don't bother with unexpected sides
            case _:
                return self.__SIDE_FALLBACK

        # No fallback allowed
        if mirror or cross:
            # Try mirror or cross fallback
            for cross_point, sides in self.__AXIS_MAP.items():
                if wanted not in sides:
                    continue

                if mirror:
                    mirror_side = sides[1] if wanted == sides[0] else sides[0]
                    return self.__deep_check_tooltip_side(mirror_side, False, cross, cross_mirror)

                return self.__deep_check_tooltip_side(cross_point, cross_mirror, False)

        return self.__SIDE_FALLBACK

    def __deep_search_widget(self, widget: Widget, type_id: str, x: float, y: float) -> Widget|None:
        """
        Recursively locate the deepest widget interested in a specific MotionEvent type.

        The search is pruned using the widget's ``motion_filter`` so only subtrees
        containing widgets registered for ``type_id`` are evaluated.
        Collision checks are performed in window-space coordinates.

        :param widget:  Root widget of the subtree being evaluated.
        :param type_id: MotionEvent type identifier (e.g. ``"hover"``, ``"touch"``).
        :param x:       X pointer position in window coordinates.
        :param y:       Y pointer position in window coordinates.
        """
        # Skip entire subtree if no child cares about this `type_id` event type
        filters: dict[str, list[Widget]] = widget.motion_filter
        if type_id not in filters:
            return None

        # Skip entire subtree if the provided point (x, y) is outside interested `widget`
        if not widget.collide_point(x, y):
            return None

        # Search children first
        for child in widget.children:
            found_widget: Widget|None = self.__deep_search_widget(child, type_id, x, y)

            if found_widget:
                return found_widget

        # If this widget itself registered for the type, return it
        if widget in filters.get(type_id, []):
            return widget

        return None

    def __get_side_size(self, wanted: str) -> int|float:
        """ Compute available space for the tooltip on the given side. """
        # Local variables
        hovered: Widget|None = self.__hovered_widget

        if hovered is None:
            return 0

        hovered_offset: int|float|None = hovered.tooltip_offset
        tooltip_offset: int|float = hovered_offset if (hovered_offset is not None) else self.tooltip_offset

        match wanted:
            case "left":
                return hovered.x - self.edge_offset[0] - tooltip_offset
            case "top":
                return self.window.height - hovered.top - self.edge_offset[1] - tooltip_offset
            case "right":
                return self.window.width - hovered.right - self.edge_offset[2] - tooltip_offset
            case "bottom":
                return hovered.y - self.edge_offset[3] - tooltip_offset

            case self.__SIDE_MAX_WIDTH:
                return self.window.width - self.edge_offset[0] - self.edge_offset[2]
            case self.__SIDE_MAX_HEIGHT:
                return self.window.height - self.edge_offset[1] - self.edge_offset[3]

        return 0

    def __get_tooltip_instance(self, ref: TooltipTemplate|type) -> TooltipTemplate|None:
        """
        Resolve a tooltip reference into an instance.

        - If ``ref`` is a class, a new instance is created if the current tooltip was not created from the same class.
        - If ``ref`` is an instance, it is reused unless it matches the existing tooltip instance.

        Return the resolved tooltip instance when a new tooltip must be used, otherwise ``None``.
        """
        if isinstance(ref, type) and not (self.__is_tooltip_from_class and ref is self.__tooltip_widget.__class__):
            self.__is_tooltip_from_class = True
            return ref()

        elif ref is not self.__tooltip_widget:
            self.__is_tooltip_from_class = False
            return cast(TooltipTemplate, ref)

        return None

    @property
    def __is_tooltip_interactive_or_near(self) -> bool:
        """ Return True if the tooltip is interactive, visible, and the pointer is hovering or near it. """
        if self.__is_tooltip_interactive:
            # If the tooltip is valid and visible
            if self.__tooltip_widget and self.__tooltip_widget.opacity > 0.0:
                pointer: tuple[float, float] = self.window.mouse_pos

                # If the pointer is hovering the tooltip, we are already interacting with it
                if self.__tooltip_widget.collide_point(*pointer):
                    return True

                # Otherwise, check if the pointer is in a safe distance near the tooltip for special cases
                match self.__last_tooltip_side:
                    case "cursor":
                        return self.__last_pointer.distance(pointer) < self.__tooltip_distance

                    case self.__SIDE_FALLBACK | self.__SIDE_FALLBACK_ZERO:
                        x: tuple[float, float, float] = (
                            self.__last_pointer.x, self.__tooltip_widget.x, self.__tooltip_widget.right
                        )
                        y: tuple[float, float, float] = (
                            self.__last_pointer.y, self.__tooltip_widget.y, self.__tooltip_widget.top
                        )
                        b_min: list[float] = [min(x), min(y)]
                        b_max: list[float] = [max(x), max(y)]

                        # Add threshold around cursor
                        if x[0] == b_max[0]:
                            b_max[0] += self.__MOVE_THRESHOLD
                        elif x[0] == b_min[0]:
                            b_min[0] -= self.__MOVE_THRESHOLD

                        if y[0] == b_max[1]:
                            b_max[1] += self.__MOVE_THRESHOLD
                        elif y[0] == b_min[1]:
                            b_min[1] -= self.__MOVE_THRESHOLD

                        return Vector.in_bbox(pointer, b_min, b_max)

                # Otherwise, check if the pointer is in a safe distance near the tooltip for specific cases
                safe: Vector = Vector(*self.__tooltip_widget.pos)

                # Solve safe position X
                match self.__last_tooltip_side:
                    case "left":
                        safe.x = self.__tooltip_widget.right
                    case "top" | "bottom":
                        safe.x = clamp(pointer[0], (self.__tooltip_widget.x, self.__tooltip_widget.right))

                # Solve safe position Y
                match self.__last_tooltip_side:
                    case "bottom":
                        safe.y = self.__tooltip_widget.top
                    case "left" | "right":
                        safe.y = clamp(pointer[1], (self.__tooltip_widget.y, self.__tooltip_widget.top))

                return safe.distance(pointer) < self.__tooltip_distance

        return False

    def __make_tooltip_visible(self, state: bool = True) -> None:
        """ Change the visibility of the tooltip widget. """
        if not state:
            self.__show_timer.cancel()

        # Rebuild the canvas when tooltip changed
        if self.__next_tooltip_widget:
            if self.__tooltip_widget:
                self.window.remove_widget(self.__tooltip_widget)

            self.window.add_widget(self.__next_tooltip_widget)
            self.__tooltip_widget = self.__next_tooltip_widget
            self.__next_tooltip_widget = None

        if self.__tooltip_widget:
            wanted_opacity: float = 1.0 if state else 0.0
            actual_opacity: float = self.__tooltip_widget.opacity
            duration: float = self.animation_time if state else clamp(self.animation_time, (0, self.delay_time))

            if wanted_opacity != actual_opacity:
                hovered: Widget|None = self.__hovered_widget

                if hovered:
                    hovered.dispatch("on_pre_tooltip", state)

                self.__animation._duration = duration
                self.__animation.animated_properties["opacity"] = wanted_opacity
                self.__animation.start(self.__tooltip_widget)

                if hovered:
                    Clock.schedule_once(lambda _,w=hovered: w.dispatch("on_tooltip", state), duration)

    def __on_leave_window(self) -> None:
        """ Reset main internal references, cancel the clock tasks and make the tooltip hidden. """
        self.__idle_timer.cancel()
        self.__make_tooltip_visible(False)
        self.__last_pointer.x = self.__last_pointer.y = -1.0
        self.__hovered_widget = None

    # noinspection PyUnresolvedReferences
    def __resolve_tooltip_widget(self) -> None:
        """
        Resolves whether a custom tooltip or the default tooltip should be used.
        Reuses the existing instance when possible, or creates a new one base on the hovered widget.
        """
        # Invalid reference or empty tooltip text
        if not self.__hovered_widget or self.__hovered_widget.tooltip_text.strip() == "":
            self.__make_tooltip_visible(False)
            return None

        # Local variables
        hovered: Widget = self.__hovered_widget
        this_tooltip: TooltipTemplate|None = None
        ref_tooltip: TooltipTemplate|type|None = hovered.tooltip_template

        # Is a custom tooltip
        if ref_tooltip:
            instance: TooltipTemplate|None = self.__get_tooltip_instance(ref_tooltip)
            if instance:
                self.__is_custom_tooltip = True
                this_tooltip = instance

        # Is previous one was a custom tooltip or this is first tooltip widget
        elif self.__is_custom_tooltip or self.__tooltip_widget is None:
            instance: TooltipTemplate|None = self.__get_tooltip_instance(self.tooltip_template)
            if instance:
                self.__is_custom_tooltip = False
                this_tooltip = instance

        # Keep current tooltip, or queue new one for pre‑fade swap
        if this_tooltip is None:
            this_tooltip = self.__tooltip_widget

        else:
            self.__next_tooltip_widget = this_tooltip

        # Make shore the tooltip is editable, but still hidden
        this_tooltip.disabled = False
        this_tooltip.opacity = 0.0

        # Update tooltip layout
        this_tooltip.update_text(hovered.tooltip_text, hovered.tooltip_markup)
        this_tooltip.update_size()

        # [ Idle mode ] Interested widget is already valid and hovered
        self.__idle_timer.cancel()

        # Solve initial tooltip interactive flag
        if hovered.tooltip_interactive is None:
            self.__is_tooltip_interactive = self.tooltip_interactive
        else:
            self.__is_tooltip_interactive = hovered.tooltip_interactive

        # Show the tooltip
        self.__solve_tooltip_side()
        self.__show_timer()

        return None

    def __update_tooltip_position(self) -> None:
        """
        Compute the final tooltip position based on the last resolved side.

        Positioning applies widget offset, safe-area offset, and centering rules.
        """
        # Local variables
        this_x: float = 0.0
        this_y: float = 0.0
        hovered: Widget|None = self.__hovered_widget
        tooltip: TooltipTemplate|None = self.__next_tooltip_widget or self.__tooltip_widget

        # Do nothing if hovered widget or tooltip widget was not solved
        if hovered is None or tooltip is None:
            return None

        # Solve FALLBACK's
        match self.__last_tooltip_side:
            case self.__SIDE_FALLBACK:
                tooltip.pos = (self.edge_offset[0], self.edge_offset[3])
                return None

            case self.__SIDE_FALLBACK_ZERO:
                tooltip.pos = (0.0, 0.0)
                return None

        # Relevant tooltip offset
        hovered_offset: int|float|None = hovered.tooltip_offset
        tooltip_offset: int|float = hovered_offset if (hovered_offset is not None) else self.tooltip_offset

        # Compute allowed tooltip distance
        self.__tooltip_distance = tooltip_offset + self.__MOVE_THRESHOLD

        # Local variables
        mouse_pos: tuple[float, float] = self.window.mouse_pos

        # Solve position X
        match self.__last_tooltip_side:
            case "left":
                this_x = hovered.x - tooltip_offset - tooltip.width

            case "right":
                this_x = hovered.right + tooltip_offset

            case "top" | "bottom":
                if tooltip.width < hovered.width:
                    this_x = mouse_pos[0] - tooltip.width * 0.5
                else:
                    this_x = hovered.x - (tooltip.width - hovered.width) * 0.5

            case "cursor":
                # By default, position on the right side of the cursor
                this_x = mouse_pos[0] + tooltip_offset

                # If the tooltip do not feet on the available space, try left side
                if (this_x + tooltip.width) > (self.window.width - self.edge_offset[2]):
                    this_x = mouse_pos[0] - tooltip_offset - tooltip.width

                    # Fallback to the actual mouse cursor
                    if this_x < self.edge_offset[0]:
                        this_x = mouse_pos[0]

        # Solve position Y
        match self.__last_tooltip_side:
            case "top":
                this_y = hovered.top + tooltip_offset

            case "bottom":
                this_y = hovered.y - tooltip_offset - tooltip.height

            case "left" | "right":
                if tooltip.height < hovered.height:
                    this_y = mouse_pos[1] - tooltip.height * 0.5
                else:
                    this_y = hovered.y - (tooltip.height - hovered.height) * 0.5

            case "cursor":
                # By default, position on the top side of the cursor
                this_y = mouse_pos[1] + tooltip_offset

                # If the tooltip do not feet on the available space, try bottom side
                if (this_y + tooltip.height) > (self.window.height - self.edge_offset[1]):
                    this_y = mouse_pos[1] - tooltip_offset - tooltip.height

                    # Fallback to the actual mouse cursor
                    if this_y < self.edge_offset[3]:
                        this_y = mouse_pos[1]

        # Set solved positions
        tooltip.pos = (
            clamp(this_x, (self.edge_offset[0], self.window.width - tooltip.width - self.edge_offset[2])),
            clamp(this_y, (self.edge_offset[3], self.window.height - tooltip.height - self.edge_offset[1])),
        )

        return None

    def __solve_tooltip_side(self) -> None:
        """ Solve if tooltip fits on the requested side and resolve a fallback if not. """
        tooltip: TooltipTemplate|None = self.__next_tooltip_widget or self.__tooltip_widget

        if tooltip is None:
            self.__last_tooltip_side = self.__SIDE_FALLBACK_ZERO

        elif tooltip.width > self.__get_side_size(self.__SIDE_MAX_WIDTH):
            self.__last_tooltip_side = self.__SIDE_FALLBACK_ZERO

        elif tooltip.height > self.__get_side_size(self.__SIDE_MAX_HEIGHT):
            self.__last_tooltip_side = self.__SIDE_FALLBACK_ZERO

        elif self.__hovered_widget:
            wanted_side: str = self.__hovered_widget.tooltip_side or self.tooltip_side

            self.__last_tooltip_side = self.__deep_check_tooltip_side(wanted_side)

        return None
