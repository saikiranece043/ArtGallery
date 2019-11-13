
import math
import random

'''
    It has been proven that being Q a polygon with r reflex vertices,
    r guards placed on the reflex vertices of Q are always sufficient and occasionally necessary to guard Q
'''

'''
This is a class to represent a genetic algorithm or atleast some aspects of it
Constructor with mandatory args reflex vertices and vertices (array of point objects)
'''


class GA:


    def __init__(self,r,nv):
        self.reflexvertices =r
        self.noofvertices=nv
        self.maxguards = math.floor(self.noofvertices/3)
        self.pop = self.initialPop()

    def set_pop(self, pop):
        self.pop = list.copy(pop)

    def initialPop(self):
        print("Initial population of individuals")
        print("No of reflex vertices %d hence going to generate individuals"%(len(self.reflexvertices)))
        print("The length of an individual would be no of vertices of the polygon i.e ",self.noofvertices)
        print("Maximum number of guards required for the gallery is ",self.maxguards)
        pop = []

        for index in range(0,len(self.reflexvertices)):
            indv = [0] * self.noofvertices
            rev = list.copy(self.reflexvertices)
            for index in range(0,self.maxguards):
                #print("reflex vertices copy",rev)
                choice = random.choice(rev)
                #print("random choice of the vertice",choice)
                indv[choice] = 1
                rev.remove(choice)
            pop.append(indv)
        return pop









