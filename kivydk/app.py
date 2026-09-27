#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 25 Sep 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
This module provides the KivyDK-specific :class:`App` implementation responsible for preparing
and maintaining the runtime environment required by KivyDK. It initializes internal managers,
registers event systems such as the :class:`PointerManager` and serves as the integration point
for framework-level features including the settings panel, theme management and tool execution utilities.

.. TODO::
    Currently it initializes the :class:`PointerManager`, but additional managers—such as
    theme controllers, settings interfaces and tool execution panels—will be integrated here
    in future versions of KiviDK.
"""
__all__ = ("App",)

#// IMPORT
from kivy.app import App as App_kivy

from kivydk.manager.pointer import PointerManager


#// LOGIC
class App(App_kivy):
    """
    KiviDK application class extending :class:`~kivy.app.App`.

    It ensures that KiviDK-specific managers are properly initialized and registered with the
    window system, allowing the framework's internal logic—such as pointer routing—to operate
    correctly during the application's lifecycle.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # Private variables
        self.__kdk_pointer_manager: PointerManager = PointerManager()

    def _run_prepare(self) -> None:
        """ Prepare the current application for the main loop. """
        super()._run_prepare()

        self.root_window.register_event_manager(self.__kdk_pointer_manager)

    def _stop(self, *args) -> None:
        """ Stop the current application by leaving the main loop. """
        self.root_window.unregister_event_manager(self.__kdk_pointer_manager)

        super()._stop(*args)
