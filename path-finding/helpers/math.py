def clamp(value: float, min_value: float, max_value: float) -> float:
    """Push values outside the range [min_value, max_value] back into the range."""
    return min(max(value, min_value), max_value)

def lerp(from_value: float, to_value: float, ratio: float) -> float:
    """Linearly interpolate between from_value and to_value."""
    return from_value + (to_value - from_value) * ratio