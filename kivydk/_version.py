#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 21 Jan 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
__all__ = (
    "MAJOR", "MINOR", "MICRO", "REVISION",
    "RELEASE", "VERSION_STRING"
)

#//| Version variables
#//|>--------------------------------------------------------<|
MAJOR: int = 0
MINOR: int = 0
MICRO: int = 6
VERSION_STRING: str = f"{MAJOR}.{MINOR}.{MICRO}"


#//| Development | Revision variables
#//|>--------------------------------------------------------<|
REVISION: int = 2
RELEASE: bool = False

# If is not the stable release, update `VERSION_STRING` to reflect that
if not RELEASE:
    VERSION_STRING.join(f".dev{max(1, REVISION)}")
elif REVISION:
    VERSION_STRING.join(f".rev{REVISION}")


#//| exec'd from setup.py ?
#//|>--------------------------------------------------------<|
__version__: str = VERSION_STRING
