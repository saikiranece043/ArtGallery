import matplotlib.pyplot as plt
from src.Point import *
from src.Polygon import *
from src.generatepoints import *
from src.GA import *
import tripy
from src.Intersection import *
import operator
import random
import time
import matplotlib.animation as ani
from matplotlib import style
import sys
import time


# point 1 and point 2 are the indexes in coords
# point 1 and 2 are the endpoints of line segment (i.e line joining reflex vertice and one of the triangulated ploygon vertice )
# this function checks if a line segments cuts the polygon or not
def intersectionofpolygon(point1, point2):
    p1 = Point(coord[point1][0], coord[point1][1])
    p2 = Point(coord[point2][0], coord[point2][1])
    status = False
    for index, point in enumerate(coord):
        if index != point1 and index != point2:
            #print("checking the line segment1 (%d,%d) and line segment 2 (%d,%d) for intersection"%(point1,point2,index,index+1))
            if index == len(coord)-1:
                if point1 != 0 and point2 != 0:
                    #print("checking the line segment1 (%d,%d) and line segment 2 (%d,%d) for intersection" % (point1, point2, index, 0))
                    p3 = Point(coord[index][0], coord[index][1])
                    p4 = Point(coord[0][0], coord[0][1])
                    status = get_line_intersection(p1, p2, p3, p4)
            else:
                if index+1 != point1 and index+1 != point2:
                    #print("checking the line segment1 (%d,%d) and line segment 2 (%d,%d) for intersection" % (point1, point2, index, index + 1))
                    p3 = Point(coord[index][0], coord[index][1])
                    p4 = Point(coord[index+1][0], coord[index+1][1])
                    status = get_line_intersection(p1, p2, p3, p4)


        if status == True:
          # print("Line segment of polygon",coord.index((p1.x,p1.y)),coord.index((p3.x,p3.y)),coord.index((p4.x,p4.y)))
           break

    return status

#finding the visibility of a reflex vertice
def findvisibility(vertice):
    visibletraingles = []
    for t in trianglep:
        if vertice in t:
            visibletraingles.append(t)
        elif intersectionofpolygon(vertice, t[0]):
            test=1
           # print("Point (%d,%d) is cutting the ploygon hence vertice can't see the traingle"%(vertice,t[0]))

        elif intersectionofpolygon(vertice, t[1]):
            test = 1
            #print("Point (%d,%d) is cutting the ploygon hence vertice can't see the traingle"%(vertice,t[0]))

        elif intersectionofpolygon(vertice, t[2]):
            test = 1
            #print("Point (%d,%d) is cutting the ploygon hence vertice can't see the traingle"%(vertice,t[0]))

        else:
            visibletraingles.append(t)

    return visibletraingles


#This function is to store the visubility of a guard placed on a reflex vertice
#This is to avoid calls everytime to the visibility which requires lot of computation
def storevisibility():
    guardvis={}
    for guard in reflexvertices:
        guardvis[guard]=findvisibility(guard)
    return guardvis


# defining the fitness of the individual
def fitness(indv):
        totalvisbility = []
        for index, guard in enumerate(indv):
            if guard == 1:
                totalvisbility= totalvisbility + dictvis[index]
        totalvisbility = list(dict.fromkeys(totalvisbility))
        #print("visibility of an indvidual %s %s" % (indv, len(totalvisbility)))
        return (len(totalvisbility)/len(traingles)) *100


#this function to rank the indviduals in the population as per the fitness values
def rankindv(population):

    fitnessresults = {}

    for idx,indv in enumerate(population):
        fit=fitness(indv)
        if fit == 100:
           fitnessresults[idx] = fit + (len(indv)-indv.count(1))
        else:
            fitnessresults[idx] = fit
    #print(fitnessresults)
    return sorted(fitnessresults.items(),key=operator.itemgetter(1),reverse=True)



'''
We can use different methods of selection tournament or roulette wheel
For this experiment we choose tournament Selection 
'''
#Selecting the top parents indexes as per the fitness values
def selectedParents(rankedpop):
    selectedParents =[]

    for i in range(0,len(rankedpop)):
        #print("best individuals in the population ",rankedpop[i][0])
        selectedParents.append(rankedpop[i][0])

    #print(selectedParents)
    return selectedParents


#Mating pool has the list of indviduals sorted on their fitness
def matingpool(population,selectedParents):
    matingPool=[]
    for index in selectedParents:
        matingPool.append(population[index])

    return matingPool






'''
Single Point crossover -- Takes the dna from the top parent, elitesize bits of top parent and concatenate with the parent from bottom pop for remaining bits
A crossover point on the parent organism string is selected. All data beyond that point in the organism string is swapped between the two parent organisms. 
'''

def crossover1(matingpool,elitesize):
     children=[]
     #print(matingpool)
     tguards = matingpool[0].count(1)
     for i in range(0,elitesize):
         children.append(matingpool[i])

     for i in range(elitesize,len(matingpool)):


         #print("before crossover %s %s"%(matingpool[0][:4],matingpool[i][4:]))
         if matingpool[0][:elitesize].count(1)+ matingpool[0][elitesize:].count(1) != tguards:
             print("the number of guards generated on crossover is not equal to the parent")


         individual= matingpool[0][:elitesize]+matingpool[i][elitesize:]
         #print("indvidual after cross over: %d %s  " %(len(individual),individual))
         children.append(individual)

     #print("children",children)
     return children

'''
Uniform crossover
Each gene (bit) is selected randomly from one of the corresponding genes of the parent chromosomes.
'''


def crossover2(matingpool,elitesize):
    children = []
    #print(matingpool)
    tguards = matingpool[0].count(1)
    for i in range(0, elitesize):
        children.append(matingpool[i])

    for i in range(elitesize, len(matingpool)):
        choice = random.randint(0,elitesize)
        # print("before crossover %s %s"%(matingpool[0][:4],matingpool[i][4:]))
        if matingpool[0][:elitesize].count(1) + matingpool[0][elitesize:].count(1) != tguards:
            print("the number of guards generated on crossover is not equal to the parent")
        indv = matingpool[i]
        #position of the guard placed in the parent
        indexofguardp = indv.index(1)
        #position of the guard placed in the eliteparent
        indexofguardep = matingpool[choice].index(1)

        if indv[indexofguardep] == 0:
            indv[indexofguardep] = 1
            indv[indexofguardp] = 0
            children.append(indv)
        else:
            children.append(indv)
        # print("indvidual after cross over: %d %s  " %(len(individual),individual))


    # print("children",children)
    return children

'''
Mutation is performed on one random indvidual which isn't part of the elite size
Mutation would remove a guard from an individual and only adds the updated individual to the population only if its unique indv in the population
The job is very simple it just flips the bits but critical as it's the only way to reduce the number of guards from the population
'''

#crossover on the bottom half i.e individuals that are not part of the elizeSize
def mutation(children,elitesize):

    randomchild = random.randint(1, elitesize)
    #randomchild2=random.randint(elitesize,len(children)-1)
    indv = children[randomchild]
    #indv2= children[randomchild2]
    children.remove(indv)
    #children.remove(indv2)
    #tmp = list.copy(children[randomchild])
    #loop =0
        #this loop is to ensure the indviduals added as children are unique
    # while True:
    #     loop = loop+1
    #     if loop == 1000:
    #             print("couldn't generate a unique individual in the population with guards",indv.count(1))
    #             break
    choice = random.choice(reflexvertices)
    #choice1= random.choice(reflexvertices)
    if indv[choice] == 1:
            #print("performed mutation")
                #print("before mutation",indv.count(1),indv)
            indv[choice] = 0
                #print("after mutation",indv.count(1),indv)

        # if indv[choice] == 0 and indv.count(1) < len(reflexvertices)/10:
        #         indv[choice] == 0
        #         indv[choice1] == 1

    #if indv2[choice] ==1:
    #   indv2[choice] =0
    # if indv not in children:
    #          print("mutation performed")
    children.append(indv)
    #children.append(indv2)
    #children.remove(tmp)
             #break
    # else:
    #         indv = tmp


    #print("After mutation",children)
    return children


'''
Aggregation of the results from the results of genetic algorithm in each generation
If the indviduals agree on 80% of the placement of guards then we retain the guard position
The other positions we shall fill by finding the min guards to co
'''


#This function is to generate children from the initial population retaining the elite size of parents
def nextgen(population,elitesize):
    #print(population)
    #print("ranked individuals",rankindv(population))
    #print("No of guards in the top rank of the population", population[rankindv(population)][0].count(1))
    sp=selectedParents(rankindv(population))
    matingPool= matingpool(population,sp)
    #print("agreement from the individuals on the pop",aggreg(matingPool))
    print("No of guards in the top rank of the population", matingPool[0].count(1),matingPool[0])
    #print("selected parents",matingPool)
    time.sleep(1)
    children = crossover1(matingPool,elitesize)
    nextgen = mutation(children,elitesize)

    #print(rankindv(nextgen))
    #print(len(rankindv(nextgen)))
    #print("size of nextgen",len(nextgen))
    return nextgen,matingPool[0]



def aggreg(population,i):
    agreement =[0]*len(population[0])
    print(agreement)
    for vertice in reflexvertices:
        for indv in population:
            if indv[vertice] == 1:
                agreement[vertice] = agreement[vertice]+1

    for vertice in reflexvertices:
        if agreement[vertice] < len(population) * 0.80:
            agreement[vertice] = 2
        else:
            agreement[vertice] = 1



    while fitness(agreement)<100:
        vis=[]
        #print("Agreement array",agreement)
        #print("visibility dict",dictvis)
        for idx,vertice in enumerate(agreement):
            if vertice == 1:
                vis=vis+dictvis[idx]
        vis = list(dict.fromkeys(vis))
        #print("visibility of the aggregated individual",vis)
        notvis = list(set(trianglep).difference(vis))
        #print("not visible traingle for the aggregated solution",notvis)
        tdict={}
        for t in notvis:
           tdict[t]=trainglefromvertices(t)

        #print("Non visibile Traingles that can be seen by the list of vertices",tdict,len(tdict))


        final={}
        for idx,vertice in enumerate(agreement):
            if vertice ==2:
                trai= set(notvis).difference(dictvis[idx])
                final[idx] = len(trai)

        finalsort=sorted(final.items(), key = operator.itemgetter(1), reverse = False)
        #print("the number of unseen traingles that other reflex vertices can see ",finalsort)

        agreement[finalsort[0][0]]=1

    # comprehensivelist=[]
    # triangleslist=[]
    # for key in tdict:
    #     comprehensivelist = comprehensivelist+list(tdict[key])
    #     triangleslist = triangleslist + list(key)
    #
    # print("List of traingles ",triangleslist)
    #
    # while not triangleslist:
    #     mostcommon=max(set(comprehensivelist),key=comprehensivelist.count)
    #     print("most common vertice that can see the triangles",mostcommon)
    #     print("Triangles this most common vertice can see is",dictvis[mostcommon])
    #     for t in dictvis[mostcommon]:
    #         if t in triangleslist:
    #            triangleslist.remove(t)

    #comprehensivelist.remove(mostcommon)

    for idx,vertice in enumerate(agreement):
        if vertice == 2:
            agreement[idx]=0





    if fitness(agreement) >= 100:
        print("Fitness of the crowd %d and number of guards %d in generation %s"%(fitness(agreement),agreement.count(1),agreement))
        return agreement




    # solution = [0]*len(population[0])
    # notvis =[]
    # vis=[]
    # for vertice in reflexvertices:
    #     if agreement[vertice]==1:
    #         notvis=notvis+dictvis[vertice]
    #     else:
    #         vis= vis+ dictvis[vertice]

    #print("Visible traingles for the aggregated result",len(dict.fromkeys(vis)),list(dict.fromkeys(vis)))




def trainglefromvertices(t):
    trvfv=[]
    for k in dictvis:
        if t in dictvis[k]:
            trvfv.append(k)
    return trvfv




#This is a draw function that is not currently used , purely used for testing
def drawpolygon(coord):
    # repeat the first point to create a 'closed loop'
    coord.append(coord[0])
    xs, ys = zip(*coord)  # create lists of x and y values


    ax1 = plt.figure().add_subplot(1, 1, 1)
    plt.plot(xs, ys)

    #
    # for tr in traingles:
    #     plt.plot([tr[0][0],tr[2][0]],[tr[0][1], tr[2][1]], 'r-.')
    #     plt.plot([tr[0][0], tr[1][0]], [tr[0][1], tr[1][1]], 'r-.')
    #     plt.plot([tr[1][0], tr[2][0]], [tr[1][1], tr[2][1]], 'r-.')

    for v in reflexvertices:

        plt.plot(coord[v][0],coord[v][1],'bo')


    for i, n in enumerate(coord):
        if i != len(coord) - 1:
            ax1.annotate(i, (xs[i], ys[i]), textcoords='data')

    #plt.show()  # if you need...

    #print("Drawing a polygon with given vertices")


#This function is not used currently was created for testing
def geneticalgo(pop,elitesize,generations):

    for i in range(0,generations):

        pop,topchoice = nextgen(pop,elitesize)


        #drawpolygon(coord)






#Below is to setup some global variables which are essential for all the functions above

'''
Generating the coordinates of the ploygon
'''
# coord = [[1,1], [3,10], [1,40], [2,80],[12,100], [12,15],[40,10]]

#coord = [(596, 133), (616, 207), (661, 181), (612, 284), (671, 236), (657, 269), (726, 263), (664, 289), (735, 318),(706, 347), (738, 389), (709, 401), (628, 338), (651, 396), (646, 477), (609, 383), (599, 421), (586, 386),(529, 450), (565, 349), (454, 436), (522, 343), (474, 326), (458, 313), (493, 282), (519, 269), (528, 245),(527, 217), (535, 207), (591, 274)]
coord=generatePolygon(800,800,600,0.6,0.2,100)
# print(coord)
#traingles = [((591, 274), (596, 133), (616, 207)), ((616, 207), (661, 181), (612, 284)), ((612, 284), (671, 236), (657, 269)), ((657, 269), (726, 263), (664, 289)), ((664, 289), (735, 318), (706, 347)), ((706, 347), (738, 389), (709, 401)), ((706, 347), (709, 401), (628, 338)), ((628, 338), (651, 396), (646, 477)), ((628, 338), (646, 477), (609, 383)), ((609, 383), (599, 421), (586, 386)), ((586, 386), (529, 450), (565, 349)), ((565, 349), (454, 436), (522, 343)), ((522, 343), (474, 326), (458, 313)), ((522, 343), (458, 313), (493, 282)), ((522, 343), (493, 282), (519, 269)), ((528, 245), (527, 217), (535, 207)), ((528, 245), (535, 207), (591, 274)), ((591, 274), (616, 207), (612, 284)), ((612, 284), (657, 269), (664, 289)), ((664, 289), (706, 347), (628, 338)), ((628, 338), (609, 383), (586, 386)), ((628, 338), (586, 386), (565, 349)), ((565, 349), (522, 343), (519, 269)), ((565, 349), (519, 269), (528, 245)), ((565, 349), (528, 245), (591, 274)), ((565, 349), (591, 274), (612, 284)), ((612, 284), (664, 289), (628, 338)), ((612, 284), (628, 338), (565, 349))]
#print(coord)


'''
Traingulating the polygon
Very important bit to calculate the visibility of a given vertice
'''


traingles = tripy.earclip(coord)
#print(traingles)
trianglep = []
for traingle in traingles:
    trianglep.append((coord.index(traingle[0]), coord.index(traingle[1]), coord.index(traingle[2])))

# print(trianglep)


# Array of points will be stored

'''
First creating Point objects for each vertice
Creating a collection of vertices and instantiating polygon obj by assigning the vertices 
'''
vertices = []
nv = len(coord)
for i in coord:
    vertices.append(Point(i[0], i[1]))

polygon = Polygon(vertices)

reflexvertices = []

totalarea = polygon.getarea(coord)
# print("Area",totalarea)

'''
Another important bit is to find out the reflex vertices in the ploygon
Because we are placing the guards only on reflex vertices
'''



for idx, point in enumerate(coord):
    # print("Calculating area by removing the point ",idx)
    vertices = coord.copy()
    vertices.remove(point)
    area = polygon.getarea(vertices)
    if totalarea < area:
        reflexvertices.append(idx)


# for reflexvertice in reflexvertices:
#      print("Visibitliy of triangle from vertice %d %d %s" % (reflexvertice,len(findvisibility(reflexvertice)),(findvisibility(reflexvertice))))
# print(reflexvertices)


'''
Visbility details for each vertice is stored in a global dictionary variable
'''

#created a visibility dictionary for each guard placed on a reflex vertice
dictvis=storevisibility()
#pop=[]

#print(dictvis)


'''
creating a GA instance ,refer to the GA class very simple class (was created for a different reason but didn't do justice)
Something to refactor for future
'''

# creating a Genetic algorithm object with reflex vertices and no of vertices of polygon as constructor arguments
ga = GA(reflexvertices, nv)
#pop=ga.pop


#pop=[[0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1], [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1], [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1], [0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1], [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1], [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1], [0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1], [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1], [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1], [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]]
#print(ga.pop)
#print(rankindv(pop))


elitesize = 4



'''
The below are matlab lib related objects necessary for plotting the graphs and points
'''
style.use('ggplot')
fig = plt.figure()
ax1= fig.add_subplot(1,1,1)

progress=[]

'''
This function is invoked by the animation object repeatedly (unfortunately only way to plot dynamically using pyplot)
This function creates generations from the functions defined above and same time updates the plots based on the values in each generation
The Plot dynamically updates for every generation and represents the top individual 
'''
def geneticalgo(i):
    #print(ga.pop)
    finalsol=[]
    sys.stdout.write("\rGeneration %i" % i)
    aggreg(ga.pop,i)
    sys.stdout.flush()

    if i == 200:
        #print("Have run 5 generations so qutting")
        plt.savefig('output'+str(i))
        plt.close(fig)

    currentpop,currenttop = nextgen(ga.pop, elitesize)
    progress.append(currenttop.count(1))
    ga.set_pop(currentpop)
    for idx,x in enumerate(currenttop):
        if x==1:
            finalsol.append(idx)
    #print("Guards should be placed on the vertices ",finalsol)

    plots=list.copy(coord)
    plots.append(plots[0])
    ax1.clear()
    xs, ys = zip(*plots)
    plt.plot(xs, ys)

    #print("current top choice",currenttop)
    for index,v in enumerate(currenttop):
        if v==1:
            plt.plot(plots[index][0], plots[index][1], 'bo')


    for i, n in enumerate(plots):
        if i != len(plots) - 1:
            ax1.annotate(i, (xs[i], ys[i]), textcoords='data')




a = ani.FuncAnimation(fig,geneticalgo,interval=1)

print(time.time())
plt.show()
#geneticalgo(pop,4,400000)

print(time.time())
#plt.close(fig)
print(progress)
plt.plot(progress)
plt.ylabel('NoofGuards')
plt.xlabel('Generation')
plt.show()
#drawpolygon(coord)
