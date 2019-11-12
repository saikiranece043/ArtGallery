# Returns 1 if the lines intersect, otherwise 0. In addition, if the lines
# intersect the intersection point may be stored in the floats i_x and i_y.


def get_line_intersection(p1, p2, p3, p4):
    xslope1 = p2.x - p1.x
    yslope1 = p2.y - p1.y

    xslope2 = p4.x - p3.x
    yslope2 = p4.y - p3.y

    if -xslope2 * yslope1 + xslope1 * yslope2 == 0:
         #print("determinant zero and the lines don't intersect")
         return False
    else:
        s = (-yslope1 * (p1.x - p3.x) + xslope1 * (p1.y - p3.y)) / (-xslope2 * yslope1 + xslope1 * yslope2)
        t = (xslope2 * (p1.y - p3.y) - yslope2 * (p1.x - p3.x)) / (-xslope2 * yslope1 + xslope1 * yslope2)

    if s >= 0 and s <= 1 and t >= 0 and t <= 1:
        return True

    else:
        return False
