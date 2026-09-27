#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 08 Jul 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|

#// IMPORT
import inspect, importlib
from types import ModuleType, FunctionType, MethodType

from kivy.properties import Property, AliasProperty, OptionProperty, VariableListProperty

from sphinx_doclang.commands import Command, cmd_self_name, cmd_self_type, _Template


#// GLOBAL VARIABLES
TAB: str = " " * 4


#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| KivyDK DocLang Commands
#//|>-----------------------------------------------------------------------------------------------------------------<|
# noinspection PyUnusedLocal
@Command.new("show code")
def cmd_show_code(*args, language: str = "python", **kwargs) -> list[str]:
    """
    Displays a code example from the ``examples/docs`` directory.

    The positional arguments are joined to form the relative path to the file.
    The ``language`` option controls the syntax highlighting used in the output.

    Usage:
        - § show code : example.py ¶
        - § show code : folder, example.cpp, language = cpp ¶
        - § show code : path/to/example.py, language = text ¶
    """
    return [
        f".. literalinclude:: /../examples/docs/{"/".join(args)}",
        f"{TAB}:language: {language}",
        f"{TAB}:linenos:"
    ]


# noinspection PyUnusedLocal
@Command.new("show image")
def cmd_show_image(*args, align: str = "center", **kwargs) -> list[str]:
    """
    Displays an image from the ``examples/docs/preview`` directory.

    The positional arguments are joined to form the relative path to the image.
    The ``align`` option controls how the image is positioned in the output.

    Usage:
        - § show image : image.png ¶
        - § show image : folder, image.png, align = left ¶
        - § show image : path/to/image.png, align = right ¶
    """
    return [
        f".. image:: /../examples/docs/preview/{"/".join(args)}",
        f"{TAB}:align: {align}"
    ]


# noinspection PyUnusedLocal
@Command.new("format")
def cmd_format(context: str, *args, style: str = "Az", **kwargs) -> str:
    """
    Generates a formatted context.

    The ``style`` option controls how the context is transformed:
        - ``AZ`` or ``upper``       → UPPERCASE
        - ``az`` or ``lower``       → lowercase
        - ``Az`` or ``capitalize``  → Capitalized
        - ``Az Az`` or ``camel``    → Camel Case (capitalize each word)

    Usage:
        - § format : my context ¶
        - § format : my context, style = upper ¶
        - § format : my context, style = None ¶
    """
    style_name: str = style.lower()

    if style == "AZ" or style_name == "upper":
        return context.upper()
    elif style == "az" or style_name == "lower":
        return context.lower()
    elif style == "Az" or style_name == "capitalize":
        return context.capitalize()
    elif style == "Az Az" or style_name == "camel":
        return " ".join([word.capitalize() for word in context.split(" ")])

    return context


# noinspection PyUnusedLocal
@Command.new("dropdown")
def cmd_dropdown(title: str = "dropdown", *args, style: str = "Az", **kwargs) -> list[str]:
    """
    Generates a simple RST dropdown content with CSS ``dk-default-value`` class for the container element.

    The ``style`` option is passed directly to the ``format`` command.

    Usage:
        - § dropdown ¶
        - § dropdown : custom title ¶
        - § dropdown : custom title, style = upper ¶
    """
    return [
        f".. dropdown:: {cmd_format(title, style=style)}",
        f"{TAB}:class-container: dk-default-value"
    ]


# noinspection PyUnusedLocal
@Command.new("code")
def cmd_code(title: str = "", line: str = "", lang: str = "Python3", *args, style: str = "Az", **kwargs) -> list[str]:
    """
    Generates the header of an RST ``code-block`` directive.
    It only produces the directive line and any configured options,
    allowing the user to place the actual code on the following lines.

    Parameters:
        - ``title``     → Optional caption displayed above the code block.
        - ``line``      → If provided, enables line numbering (``:linenos:``).
        - ``lang``      → The syntax highlighting language for the code block.
        - ``style``     → Formatting style applied to the caption.
        - ``**kwargs``  → Additional code-block options.

    Usage:
        - § code ¶
        - § code : my code, style = camel ¶
        - § code : my code, lang = CPP ¶
        - § code : my code, _, CPP ¶
        - § code : lang = doscon, class = no-copybutton ¶
    """
    compute: list[str] = [f".. code-block:: {lang}"]

    if title:
        compute.append(f"{TAB}:caption: {cmd_format(title, style=style)}")
    if line:
        compute.append(f"{TAB}:linenos:")
    for key, value in kwargs.items():
        compute.append(f"{TAB}:{key}: {value}")

    return compute


# noinspection PyUnusedLocal
@Command.new("parameters")
def cmd_parameters_list(*args, title: str = "parameters", style: str = "Az", **kwargs) -> list[str]:
    """
    Creates a **Parameters** dropdown panel.

    Keyword arguments are interpreted as parameter–description pairs and displayed as a two‑column list.

    Usage:
        - § parameters ¶
        - § parameters : param_1 = Some description., param_2 = Another description. ¶
    """
    return [
        *cmd_dropdown(title, style=style),
        "",
        f"{TAB}.. list-table::"
        f"{TAB * 2}:header-rows: 0",
        "",
        f"{TAB * 2}* - Name",
        f"{TAB * 2}  - Description",
        *cmd_parameters_item(**kwargs)
    ]


# noinspection PyUnusedLocal
@Command.new("param")
def cmd_parameters_item(*args, **kwargs) -> list[str]:
    """
    Adds parameter entries to the list generated by the ``parameters`` command.

    Keyword arguments are interpreted as parameter–description pairs.

    Usage:
        - § parameters ¶
        - § param : param_A = Description for A., param_B = Description for B. ¶
    """
    return [f"{TAB * 2}* - {f'\n{TAB * 2}  - '.join(kw)}{'' if kw[1].endswith('.') else '.'}" for kw in kwargs.items()]


# noinspection PyUnusedLocal
@Command.new("variable list use")
def cmd_variable_list_use(use: str = "default", *args, **kwargs) -> str:
    """
    Generates a description for the use case of a Kivy VariableListProperty.

    The ``use`` option controls how the context is computed to inform the
    amount of accepted values and the extended order of their use:
        - ``h`` or ``horizontal``   → two values ``[left, right]``
        - ``v`` or ``vertical``     → two values ``[top, bottom]``
        - ``d`` or ``default``      → four values ``[left, top, right, bottom]``

    Usage:
        - § variable list use ¶
        - § variable list use : H ¶
        - § variable list use : vertical ¶
    """
    use_short: str = use.upper()
    use_long: str = use.lower()
    values: str = "one %s values"
    expanded: str = "These are expanded into a list of %s values: ``[%s]``"

    if use_short == "D" or use_long == "default":
        values = values % ", two or four"
        expanded = expanded % ("four", "left, top, right, bottom")

    elif use_short == "H" or use_long == "horizontal":
        values = values % "or two"
        expanded = expanded % ("two", "left, right")

    elif use_short == "V" or use_long == "vertical":
        values = values % "or two"
        expanded = expanded % ("two", "top, bottom")

    return f"The :attr:`{cmd_self_name()}` may be specified as {values}. {expanded}."


# noinspection PyUnusedLocal
@Command.new("default value")
def cmd_default_value(value: str, *args, **kwargs) -> list[str]:
    """
    Generates a Python3 code-block as description for the provided value ready to be copied.

    Usage:
        - § default value : 28 ¶
        - § default value : '[July, 05, 2026]' ¶
    """
    return [
        *cmd_code("default value"),
        "",
        f"{TAB}{value}"
    ]


# noinspection PyUnusedLocal
@Command.new("alias property value")
def cmd_alias_property_value(cls: str, value: str, *args, **kwargs) -> list[str]:
    """
    Generates a description for the default value of a Kivy AliasProperty.

    If any extra argument is provided, the property is marked as ``read-only``.
    The actual value or number of arguments does not matter.
    Providing an extra argument simply acts as a flag to request the ``read-only`` label.

    Usage:
        - § alias property value : float, 1.0 ¶
        - § alias property value : bool, False, _ ¶
    """
    alias: str = f"{'read-only' if args else ''} :class:`~kivy.properties.AliasProperty`".lstrip(" ")

    return [
        f":attr:`{cmd_self_name()}` is a {alias} that returns a :class:`{cls}`.",
        "",
        *cmd_default_value(value)
    ]


# noinspection PyUnusedLocal, PyBroadException
@Command.new("extract default value")
def cmd_extract_default_value(*args, **kwargs) -> list[str]:
    """
    Automatically extracts the default value of the current attribute.

    This command inspects the current object's attribute, detects the class type and retrieves its default value
    directly from the attribute instance.

    The Kivy AliasProperty is intentionally excluded, as its default value cannot be safely determined
    during documentation generation.

    Usage:
        - § extract default value ¶
    """
    #|>────┐----------------------------------------------------------------------------------------------------------<|
    #│  1  │ Make shore the default value can be safely computed
    #|>────┘----------------------------------------------------------------------------------------------------------<|
    prop: object|None = _Template.OBJ        # DocLang 26.9.18

    if prop is None or isinstance(prop, AliasProperty):
        return []

    #|>────┐----------------------------------------------------------------------------------------------------------<|
    #│  2  │ Special cases
    #|>────┘----------------------------------------------------------------------------------------------------------<|
    # Kivy → VariableListProperty
    if isinstance(prop, VariableListProperty):
        try:
            default_length: int = max(1, len(prop.defaultvalue))
            return cmd_default_value(
                str([prop.defaultvalue[index % default_length]
                     for index in range(prop.length)])
            )
        except Exception:
            return cmd_default_value(str(prop.defaultvalue))

    #|>────┐----------------------------------------------------------------------------------------------------------<|
    #│  3  │ Common cases
    #|>────┘----------------------------------------------------------------------------------------------------------<|
    # Reusable variable
    extra_content: list[str] = []
    default_value: str = ""

    # Kivy → OptionProperty
    if isinstance(prop, OptionProperty):
        extra_content = [
            *cmd_dropdown("options"),
            "",
            f"{TAB}Below are listed all the available options for this attribute.",
            "",
        ]
        for option in prop.options:
            extra_content.extend([
                f"{TAB}.. code-block:: Python3",
                "",
                f'{TAB * 2}"{option}"' if isinstance(option, str) else f"{TAB * 2}{option}",
                "",
            ])

    # Kivy → Property (general class)
    if isinstance(prop, Property):
        default_value = f'"{prop.defaultvalue}"' if isinstance(prop.defaultvalue, str) else str(prop.defaultvalue)

    # Python attribute
    else:
        default_value = f'"{prop}"' if isinstance(prop, str) else str(prop)

    return [
        *extra_content,
        *cmd_default_value(default_value)
    ]


# noinspection PyUnusedLocal, PyBroadException
@Command.new("extract events")
def cmd_extract_events(*args, **kwargs) -> list[str]:
    """
    Extracts the list of events from the current object's class and generates
    a dropdown containing each event name and the first sentence of its docstring.

    Usage:
        - § extract events ¶
    """
    events: dict[str, str] = {}
    class_path: str = cmd_self_name("dotted name")

    #|>────┐----------------------------------------------------------------------------------------------------------<|
    #│  1  │ Make shore the object type is a class
    #|>────┘----------------------------------------------------------------------------------------------------------<|
    if not cmd_self_type() == "class":
        return [
            f"{TAB}[ DocLang Warning | command → extract events ]",
            f"{TAB * 2}The object ``{cmd_self_name()}`` is a ``{cmd_self_type()}`` type.",
            f"\n{TAB * 2}The ``extract events`` command is designed to work only with objects of ``class`` type."
        ]

    #|>────┐----------------------------------------------------------------------------------------------------------<|
    #│  2  │ Import the class object from the dotted path
    #|>────┘----------------------------------------------------------------------------------------------------------<|
    try:
        module_name, class_name = class_path.rsplit(".", 1)
        module: ModuleType = importlib.import_module(module_name)
        cls: type = getattr(module, class_name)
    except Exception:
        return []

    #|>────┐----------------------------------------------------------------------------------------------------------<|
    #│  3  │ Read ``__events__`` from the class
    #|>────┘----------------------------------------------------------------------------------------------------------<|
    available_events: list[str] | tuple[str] = cls.__dict__.get("__events__", [])

    if not isinstance(available_events, (list, tuple)):
        return []

    #|>────┐----------------------------------------------------------------------------------------------------------<|
    #│  4  │ Extract first sentence of each event method's docstring
    #|>────┘----------------------------------------------------------------------------------------------------------<|
    for event_name in available_events:
        method: FunctionType | MethodType | None = getattr(cls, event_name, None)

        if method is None:
            continue

        # Clean docstring and extract the first sentence only (inspect removes indentation)
        doc: str = inspect.getdoc(method) or ""
        first_sentence: str = doc.split(".", 1)[0].strip()

        if first_sentence and not first_sentence.endswith("."):
            first_sentence += "."

        events[event_name] = first_sentence

    #|>────┐----------------------------------------------------------------------------------------------------------<|
    #│  5  │ Build the dropdown output
    #|>────┘----------------------------------------------------------------------------------------------------------<|
    if events:
        return [
            *cmd_dropdown("events"),
            "",
            f"{TAB}.. TODO::",
            f"{TAB * 2}The current event implementation relies on ``__events__`` being defined as a class attribute.",
            f"{TAB * 2}This works for now, but it overrides inherited Kivy events.",
            "",
            f"{TAB * 2}When revisiting the event system, consider migrating to ``register_event_type()``",
            f"{TAB * 2}and updating the DocLang command to support dynamically registered events.",
            "",
            *[f"{TAB}:meth:`{f"`\n{TAB * 2}".join(event)}" for event in events.items()]
        ]

    # Return an empty list if no events was found
    return []


@Command.new("evaluate")
def cmd_evaluate(*args, _end_: str="", **kwargs) -> list[str]:
    """
    Evaluate the current documentation object with the given arguments and
    return a formatted code block showing both the call and its evaluated result.

    The ``_end_`` option is used to append text after the result line.

    Usage:
        - § evaluate : some, arguments ¶
        - § evaluate : related, arguments, _end_ = some appended information ¶
    """
    arguments: str = ', '.join([*args, *[f"{k}={w}" for k,w in kwargs.items()]])
    return [
        ".. code-block:: Python3",
        "",
        f"{TAB}{cmd_self_name()}({arguments})",
        f"{TAB}# {eval(
            f"OBJ({arguments})", {
                "OBJ": _Template.OBJ
            }
        )}"
        f"{TAB if _end_ else ''}{_end_}",
    ]
