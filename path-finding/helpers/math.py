def clamp(value: float, min_value: float, max_value: float) -> float:
    """Push values outside the range [min_value, max_value] back into the range."""
    return min(max(value, min_value), max_value)
