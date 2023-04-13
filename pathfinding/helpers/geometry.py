def wkt_rect(startCorner: tuple[int, int], oppositeCorner: tuple[int, int], padding=0) :
    """
    Generate a WKT rectangular POLYGON between two corners.
    
    Padding may be added to increase the area.
    """

    # The distance between the points
    horizontal_dist = abs(startCorner[0]-oppositeCorner[0])
    vertical_dist = abs(startCorner[1]-oppositeCorner[1])

    # The corners of the area we want to download
    left = int(min(startCorner[0], oppositeCorner[0]) - horizontal_dist*padding)
    right = int(max(startCorner[0], oppositeCorner[0]) + horizontal_dist*padding)
    up = int(max (startCorner[1], oppositeCorner[1]) + vertical_dist*padding)
    down = int(min(startCorner[1], oppositeCorner[1]) - vertical_dist*padding)

    return f"POLYGON(({left} {down}, {left} {up}, {right} {up}, {right} {down}, {left} {down}))"