# Returns 1 if the lines intersect, otherwise 0. In addition, if the lines
# intersect the intersection point may be stored in the floats i_x and i_y.
'''
This function is to check if a line segment(p1,p2) intersects with a line segment (p3,p4)
'''

def get_line_intersection(p1, p2, p3, p4):
    xslope1 = p2.x - p1.x
    yslope1 = p2.y - p1.y

    xslope2 = p4.x - p3.x
    yslope2 = p4.y - p3.y




    if -xslope2 * yslope1 + xslope1 * yslope2 == 0:
         print("determinant zero and the lines don't intersect")
         return False

    else :
        A1 = yslope1 / xslope1
        A2 = yslope2 / xslope2
        if A1 == A2:
            return False
        else:
            b1 = p1.y - A1 * p1.x
            b2 = p3.y - A2 * p3.x
            Xa = (b2 - b1) / (A1 - A2)
            if ((Xa < max(min(p1.x, p2.x), min(p3.x, p4.x))) or (Xa > min(max(p1.x, p2.x), max(p3.x, p4.x)))):
                return False
            else:
                return True

