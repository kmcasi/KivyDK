#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 14 Apr 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|

#// IMPORT
from pathlib import Path
import os


#// GLOBAL VARIABLES
TITLE: dict[str, str] = {
    "api": "API Reference",
    "uix": "UIX",
}


#// LOGIC
class Unwanted:
    Folder: list[str] = ["__pycache__", "__ref", "data", "examples", "tools"]
    File: list[str] = ["_version", "logger", "debug"]


def compute_toctree(folder: str, hidden: bool = False) -> str:
    return f".. toctree::\n\t{":hidden:" if hidden else ":maxdepth: 1"}\n\t:glob:\n\n\t{folder}/*"


def compute_automodule(module_path: str, ignore_module_all: bool = False) -> str:
    return f".. automodule:: {module_path}{"\n\t:ignore-module-all:" if ignore_module_all else ""}"


def generate_rst_tree(dir_source: str | Path, dir_output: str | Path) -> None:
    """
    Walk a Python project and generate a mirrored RST tree.
    Each .py file becomes a .rst file with the same name.

    :param dir_source: Root of the Python project.
    :param dir_output: Root where RST files will be written.
    """
    dir_source = Path(dir_source).resolve()
    dir_output = Path(dir_output).resolve()

    for root, dirs, files in os.walk(dir_source):
        root_path: Path = Path(root)

        # Skip unwanted directories
        dirs[:] = [d for d in dirs if d not in Unwanted.Folder]

        # Compute mirrored output folder
        relative: Path = root_path.relative_to(dir_source)
        rst_folder: Path = dir_output / relative
        rst_folder.mkdir(parents=True, exist_ok=True)

        # Generate RST for each .py file
        for file in files:
            file_name: str = Path(file).stem
            # Ignore unwanted files
            if not file.endswith(".py") or file_name in Unwanted.File:
                continue
            # Ignore private files except "__init__.py" ones
            elif file.startswith("_") and file_name != "__init__":
                continue

            if file_name == "__init__":
                if rst_folder == dir_output:
                    module_name: str = list(TITLE.keys())[0]
                    module_path: str = dir_source.name
                    rst_name: str = f"{module_name}.rst"
                    module_content: str = (
                        f"{compute_automodule(module_path)}\n\n"
                        f"{"~" * 4}\n\nContents\n{"-" * len("Contents")}\n\n"
                        f"{compute_toctree(rst_folder.name)}"
                    )
                else:
                    module_name: str = relative.stem
                    module_path: str = (dir_source.name / relative).as_posix().replace("/", ".")
                    rst_name: str = f"{Path(root).stem.lower()}.rst"
                    module_content: str = (
                        f"{compute_automodule(module_path, True)}\n\n"
                        f"{compute_toctree(rst_name[:-4])}"
                    )

                rst_path: Path = rst_folder.parent / rst_name

            else:
                rst_name: str = f"{file[:-3]}.rst"
                rst_path: Path = rst_folder / rst_name
                module_name: str = file_name
                module_path: str = (dir_source.name / relative / file[:-3]).as_posix().replace("/", ".")
                module_content: str = compute_automodule(module_path)

            # Write RST file
            title: str = TITLE[module_name] if module_name in TITLE else " ".join(
                [word.capitalize() for word in module_name.split("_")]
            )
            content: str = (
                f"{title}\n{"=" * len(title)}"
                f"\n\n{module_content}"
            )

            rst_path.write_text(content, encoding="UTF-8")

        #     print(f"[FILE] {root}/{file}")
        #     print("[Title]", title, "||", module_name, "|", dir_source.name)
        #     print("rst_path", rst_path)
        #     print(content)
        #     print(f"|{'-'*21}|")
        # print("")


#// RUN
if __name__ == "__main__":
    PATH_SCRIPT = Path(__file__).resolve().parents

    generate_rst_tree(
        dir_source = PATH_SCRIPT[1] / "kivydk",
        dir_output = PATH_SCRIPT[1] / "documentation" / "api"
    )
    print("[ DONE ]")
