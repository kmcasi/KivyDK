#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 12 Sep 2022. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
Helpers used throughout KiviDK for value manipulation, scaling and normalization.
These functions provide small, reliable primitives for common numeric operations.

They are intended to support UI logic, animations, visualizers and any component that
needs consistent numeric transformations without relying on external libraries.
"""
__all__ = (
    "clamp",
    "normalize", "normalize_relative",
    "remap_range"
)


#// LOGIC
def clamp(value: int|float, bounds: tuple[int|float, int|float] = (0, 1)) -> int|float:
    """
    Constrain a numeric value to the inclusive range defined by ``bounds``.
    The bounds are automatically ordered.

    § parameters : value = The value to clamp, bounds = A tuple containing two numeric limits ¶

    § dropdown : Example ¶
        § evaluate : -2 ¶
        § evaluate : 2, bounds=(4/, 6) ¶
        § evaluate : 10, bounds=(5/, 2), _end_="(bounds become [2, 5])" ¶
    """
    b_min, b_max = min(bounds), max(bounds)
    return max(b_min, min(value, b_max))


def normalize(value: int|float, bounds: tuple[int|float, int|float] = (0, 1), digits: int = 8) -> int|float:
    """
    Map a numeric value from the range defined by ``bounds`` into the normalized range.
    The bounds are automatically ordered and the result is not clamped.

    § parameters : value = The value to normalize ¶
    § param : bounds = A tuple containing two numeric limits ¶
    § param : digits = Maximum fractional digits ¶

    § dropdown : Example ¶
        § evaluate : 1, bounds=(0/, 2) ¶
        § evaluate : 2, bounds=(5/, 1), _end_="(bounds become [1, 5])" ¶
        § evaluate : -2, bounds=(2/, 0), _end_="(bounds become [0, 2])" ¶
    """
    b_min, b_max = min(bounds), max(bounds)
    division: int|float = b_max - b_min
    return 0 if (division == 0) else b_min if (b_min == b_max) else round((value - b_min) / division, digits)


def normalize_relative(*values: int|float, scale: int|float = 1, digits: int = 8) -> list[float]:
    """
    Normalize a sequence of numeric values relative to their maximum value.
    Each result is in the range ``[0, scale]``.

    Useful for visualizers, meters or any context where values must be
    expressed as proportions of the largest value.

    § parameters : values = The values to normalize ¶
    § param : scale = The upper bound of the normalized range ¶
    § param : digits = Maximum fractional digits ¶

    § dropdown : Example ¶
        § evaluate : 1, 2, 3, 4, 5 ¶
        § evaluate : 1, 2, 3, 4, 5, scale=2 ¶
        § evaluate : 1-1, -2, -3, -4, -5 ¶
    """
    relative_max: int|float = max(values)

    if relative_max <= 0:
        relative_max = min(values)
        scale *= (-1)

    if scale == 0 or relative_max == 0:
        return [0 for _ in range(len(values))]

    return [round(value / relative_max * scale, digits) for value in values]


def remap_range(*values: int|float, actual: tuple[int|float, int|float], desired: tuple[int|float, int|float] = (0, 1),
                digits: int | None = None) -> list[int|float]:
    """
    Map numeric values from an actual range into a desired range.

    Values outside the actual range will produce results outside the desired
    range. Useful for UI scaling, visualizers, animations, and any context
    where values must be expressed in a different numeric domain.

    § parameters : values = Values to remap ¶
    § param : actual = Source range (min, max), desired = Target range (min, max) ¶
    § param : digits = Optional rounding precision ¶

    § dropdown : Example ¶
        § evaluate : 1, 2, 3, 4, 5, actual=(1/, 5) ¶
        § evaluate : 1, 2, 3, 4, 5, 6, 7, 8, actual=(3/, 7), desired=(0/, 2) ¶
    """
    a_min, a_max = min(actual), max(actual)
    d_min, d_max = min(desired), max(desired)
    division: int|float = a_max - a_min

    if division == 0:
        out_value: int|float = round(d_min, digits) if digits is not None else d_min
        return [out_value for _ in values]

    results: list[int|float] = [d_min + (value - a_min) * (d_max - d_min) / division for value in values]

    return [round(v, digits) for v in results] if digits is not None else results
