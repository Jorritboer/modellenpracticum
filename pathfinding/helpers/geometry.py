def wkt_rect_from_corners(start_corner: tuple[int, int], opposite_corner: tuple[int, int], padding=0) -> str :
    """
    Generate a WKT rectangular POLYGON between two corners.
    
    Padding may be added to increase the area.
    """

    # The distance between the points
    horizontal_dist = abs(start_corner[0]-opposite_corner[0])
    vertical_dist = abs(start_corner[1]-opposite_corner[1])

    # The corners of the area we want to download
    left = int(min(start_corner[0], opposite_corner[0]) - horizontal_dist*padding)
    right = int(max(start_corner[0], opposite_corner[0]) + horizontal_dist*padding)
    up = int(max (start_corner[1], opposite_corner[1]) + vertical_dist*padding)
    down = int(min(start_corner[1], opposite_corner[1]) - vertical_dist*padding)

    return f"POLYGON(({left} {down}, {left} {up}, {right} {up}, {right} {down}, {left} {down}))"