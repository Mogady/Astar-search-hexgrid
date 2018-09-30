import collections
import sys
class honeycomb:
    def __init__(self,input):
        self.d = collections.defaultdict(dict)
        self.input=input.split('\n')[0]
        self.IDs=input.split('\n')[1]
        self.R=int(self.input.split()[0])
        self.N=int(self.input.split()[1])
        self.A=int(self.input.split()[2])
        self.B=int(self.input.split()[3])
        self.X=int(self.input.split()[4])
    #constructing the grid as dictionary of dictionaries with each row have dictionary of cells
    def grid(self,num=0):
        k=self.R
        for i in range(self.R):
            for x in range(k):
                self.d[i][str(x+num)]=x+num
            k+=1
            num=x+num+1
        for i in range(self.R-1):
            for x in range(k-2):
                self.d[i+self.R][str(x+num)]=x+num
            k-=1
            num=x+num+1 
    #fill the grid with 0 if no block or 1 if ther is a blocking cell
    def fill(self):
        for key,val in self.d.items():
            for k,v in val.items():
                self.d[key][k]=0
        for id in self.IDs.split():
            for key,val in self.d.items():
                if id in val.keys():
                    self.d[key][id]=1
    #simple function that check for valid condition of the cell
    def check(self,cell):
        for key,val in self.d.items():
            if (cell in val.keys()) :
                if self.d[key][cell]!=1:
                    return key,len(val.keys())

    #get the neighbours of the cell in the hex grid
    def get_neighbours(self,cell):
        neighbours=[]
        if(self.check(str(cell))):
            key,row_num=self.check(str(cell))
            if row_num:
                if self.check(str(cell+row_num)):
                    neighbours.append(cell+row_num)
                if self.check(str(cell+row_num+1)):
                    neighbours.append(cell+row_num+1) 
                if self.check(str(cell-row_num)):
                    neighbours.append(cell-row_num)
                if self.check(str(cell-(row_num-1))):
                    neighbours.append(cell-(row_num-1))      
                if ( str(cell+1) in self.d[key]):
                    if  (self.d[key][str(cell+1)]!=1 ):
                        neighbours.append(cell+1)
                if ( str(cell-1) in self.d[key] ):
                    if  ( self.d[key][str(cell-1)]!=1 ):
                        neighbours.append(cell-1)        
        return neighbours

class Node:
    def __init__(self,value,point):
        self.value = value
        self.point = point
        self.parent = None
        self.H = 0
        self.G = 0
    def move_cost(self,other):
        return 0 if self.value == '.' else 1
#def h function that approximate distance between 2 points using manhatten metric
def manhattan(point,point2):
    return abs(point.point[0] - point2.point[0]) + abs(point.point[1]-point2.point[0])

def aStar(start, goal, grid):
    #The open and closed sets
    openset = set()
    closedset = set()
    #Current point is the starting point
    current = start
    #Add the starting point to the open set
    openset.add(current)
    #While the open set is not empty
    while openset:
        #Find the item in the open set with the lowest G + H score
        current = min(openset, key=lambda o:o.G + o.H)
        #If it is the item we want, retrace the path and return it
        if current == goal:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]
        #Remove the item from the open set
        openset.remove(current)
        #Add it to the closed set
        closedset.add(current)
        #Loop through the node's children/siblings
        children=[grid[x] for x in c.get_neighbours(current.point[1])]
        for node in children:
            #If it is already in the closed set, skip it
            if node in closedset:
                continue
            #Otherwise if it is already in the open set
            if node in openset:
                #Check if we beat the G score 
                new_g = current.G + current.move_cost(node)
                if node.G > new_g:
                    #If so, update the node to have a new parent
                    node.G = new_g
                    node.parent = current
            else:
                #If it isn't in the open set, calculate the G and H score for the node
                node.G = current.G + current.move_cost(node)
                node.H = manhattan(node, goal)
                #Set the parent to our current item
                node.parent = current
                #Add it to the set
                openset.add(node)
    #Throw an exception if there is no path
    return []


inpu=sys.stdin.readlines()
inpu=(''.join(inpu))
c=honeycomb(inpu)
c.grid()
c.fill()
grid=[]
for key,val in c.d.items():
    for k,v in val.items():
        grid.append( Node(c.d[key][k],(key,int(k))))

grid[c.B-1].value='.'
path = aStar(grid[c.A-1],grid[c.B-1],grid)
if(len(path)>c.N) | (len(path)==0):
    sys.stdout.write('No')
else: 
    print(len(path)) 