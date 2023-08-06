def heronShortestPath(
    x1,
    y1,
    x2,
    y2,
    ):
    if y1 == 0 or y2 == 0 or y2 > 0 and y1 < 0 or y2 < 0 and y1 > 0:
        raise ValueError("Please make sure you've entered non-zero values and make sure you've chosen both of your coordinates in one side of the river."
                         )
    else:
        if y1 > 0 and y2 > 0 or y1 < 0 and y2 < 0:
            if abs(y1) <= abs(y2):
                if x1 < x2:
                    return abs(x2 - x1) * y1 / (y1 + y2) + x1
                elif x1 > x2:
                    return x1 - abs(x2 - x1) * y1 / (y1 + y2)
            elif abs(y1) > abs(y2):
                if x1 > x2:
                    return abs(x2 - x1) * y2 / (y1 + y2) + x2
                elif x2 > x1:
                    return x2 - abs(x2 - x1) * y2 / (y2 + y1)
