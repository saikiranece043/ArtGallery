'''
A Simple Class to represent a 2d point with an x and y coordinate
'''

class Point:

    def __init__(self,x,y):
          self.x = x
          self.y= y


    def __str__(self):
        return "Point (%f,%f)" %(self.x,self.y)


   # calcuate the distance between two point objects

