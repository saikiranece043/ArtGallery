'''
A class to represent a ploygon wit attributes as vertices (collection of point objects)
The methods getreflex vertices would help us to calculate the convex vertices in the polygon
getArea is  to calc area of the polygon
calcdist is to calc distance between 2 points
'''

from src.Point import *
import math
class Polygon:

    def __init__(self,vertices):
        self.vertices = vertices

    # interior angle between its two incident edges is greater than 180 degress

    def calcdistance(self, a, b):

        xdiff = a.x - b.x
        ydiff = a.y - b.y
        distance = math.sqrt(xdiff * xdiff + ydiff * ydiff)
        return distance


    #given three points
    #(x1y2+x2y3+x3y1) - (x2y1+x3y2+x1y3)/2
    def getarea(self,vertices):
        sum1=0
        sum2=0
        for i in range(len(vertices)):
            if i == len(vertices) -1:
                sum1 = sum1 + vertices[i][0] * vertices[0][1]
            else :
                sum1 = sum1 + vertices[i][0] * vertices[i+1][1]

        for i in range(len(vertices)):
            if i == len(vertices) - 1:
                sum2 = sum2 + vertices[i][1] * vertices[0][0]
            else:
                sum2 = sum2 + vertices[i][1] * vertices[i+1][0]

        return (sum1 - sum2)/2




    def getreflexvertices(self):
        reflexvertices =[]


        print("no of reflex vertices in the polygon")
        for index in range(0,len(self.vertices)):
            if index == 0:
                A = self.vertices[index]
                B = self.vertices[index+1]
                C = self.vertices[-1]
            elif index == len(self.vertices)-1:
                A = self.vertices[index]
                B = self.vertices[index - 1]
                C = self.vertices[0]

            else:
                A = self.vertices[index]
                B = self.vertices[index+1]
                C = self.vertices[index-1]


            c = self.calcdistance(A,B)
            a = self.calcdistance(B,C)
            b = self.calcdistance(C,A)

            num = (b*b+c*c)- (a*a)
            den = 2*b*c
            angle = math.degrees(math.acos(num/den))
            print("Angle %f %s" %(angle,index))
            if angle > 180 :
                reflexvertices.append(index)

        return reflexvertices






