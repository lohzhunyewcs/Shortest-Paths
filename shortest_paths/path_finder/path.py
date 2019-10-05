# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 22:05:23 2018

@author: ZY
"""

class MinHeap(object):
    """
    Using array
    TODO: make one with Nodes
    """
    def __init__(self, items):
        self.list = []
        for item in items:
            self.insert(item)
    
    def insert(self, item):
        self.list.append(item)
        index = len(self.list) - 1
        self.floatUp(index)
    
    def decreaseVal(self, index, new):
        self.list[index] = new
        self.decreaseKey(index)
    
    def decreaseKey(self, index):
        """
        modify vertex function to do -
        """
        self.floatUp(index)
    
    def floatUp(self, index):
        done = False
        self.list[index].index = index
        while not done:
            if index == 0:
                break
            if (index - 1)%2 == 0: #if 2i + 1 = index
                parent = int((index - 1) / 2)
                if index >= len(self.list):
                    done = True
                    break
                if self.list[parent] > self.list[index]:
                    self.list[index].index = parent
                    self.list[parent].index = index
                    self.list[parent], self.list[index] = self.list[index], self.list[parent]
                else:
                    done = True
                    break
            elif (index - 2)%2 == 0:#2i+2 = index
                parent = int((index - 2) / 2)
                if index >= len(self.list):
                    done = True
                    break
                if self.list[parent] > self.list[index]:
                    self.list[index].index = parent
                    self.list[parent].index = index
                    self.list[parent], self.list[index] = self.list[index], self.list[parent]
                else:
                    done = True
                    break
            else:
                raise Exception
            index = parent
            
    def remove(self, item):
        """
        TODO: Check if greater than parent node
        """
        if item not in self.list:
            return False
        index = self.list.index(item)
        self.list[index], self.list[-1] = self.list[-1], self.list[index]
        self.list[-1].index = None
        self.list.pop()
        if len(self.list) > 0:
            self.floatUp(index)
            self.sink(index)
    
    def sink(self, index):
        done = False
        self.list[index].index = index
        while not done:
            left = int(2* (index) + 1 )
            right = int(2 *(index) + 2)
            if left < 0 or right < 0 or left >= len(self.list) or right >= len(self.list):
                done = True
#                print(left, right)
                break
#            print('remove',self.list, right, left, len(self.list))
            if self.list[left] <= self.list[right]:
#                print('moved1')
                if self.list[index] > self.list[left]:
                    self.list[index].index = left
                    self.list[left].index = index
                    self.list[index], self.list[left] = self.list[left], self.list[index]
                    index = left
                else:
                    done = True
#                    print('break2')
                    break
            elif self.list[left] > self.list[right]:
#                print('moved2')
                if self.list[index] > self.list[right]:
                    self.list[index].index = right
                    self.list[right].index = index
                    self.list[index], self.list[right] = self.list[right], self.list[index]
                    index = right
                else:
                    done = True
#                    print('break3')
                    break   
#        self.list[index].index = index
    
    def getMin(self):
        item = self.list[0]
        self.remove(item)
        return item

    def isEmpty(self):
        return len(self.list) == 0


class Graph(object):
    """
    
    TODO: Documentation
        - create edges lists so can do floyd and bellman when moving to a new file
    """
    def __init__(self, maxID):
        self.vertexCounter = 0
        self.vertices = []
        for i in range(maxID + 1):
            self.vertices.append(Vertex(i))
        self.start = [None, None]
        self.end = [None, None]
        
    def addVertex(self, vertex):
        self.vertices[vertex.id] = vertex
    
    def addEdge(self, srcID, destID, weight):
        """
        src, dest are vertex IDs
        """
        src = self.vertices[srcID]
        dest = self.vertices[destID]
        src.addEdge(Edge(src, dest, weight))
        dest.addEdge(Edge(dest, src, weight))
    
    def setCustomerHouse(self, ID):
        try:
            self.vertices[ID].isCustomer = True
            return 'Done'
        except IndexError:
            return 'Not Found'
    
    def insertCustomers(self, customers):
        """
        Assumes customer is a list of vertex IDs which are customers
        """
        for index in customers:
            self.vertices[index].isCustomer = True
        return
    
    def dijkstra(self, src, dest):
        """
        src, dest = vertex IDs
        """
        self.start[times] = src
        self.end[times] = dest
        self.vertices[src].dist[times] = 0
        queue = MinHeap(self.vertices)
        while not queue.isEmpty() and queue.list[0].dist != float('inf'): #change or min not infinity
            minVertex = queue.getMin()
            for edge in minVertex.edges:
                if minVertex.dist[times] + edge.weight < edge.dest.dist[times]:
                    edge.dest.dist[times] = minVertex.dist[times] + edge.weight
                    edge.dest.ances[times] = minVertex
                    queue.decreaseKey(edge.dest.index) #(item, new)
#        print('done')#remove when done debugging world        
        
    def getPath(self, vertex = None, count = 0):
        """
        Mabe use a linked list?
        returns (dist, path) -> (int, list)
        """
        if not self.start[times] and not self.end[count]:
            return 'Dijkstra not done!'
        if vertex is None:
            vertex = self.vertices[self.end[count]]
        else:
            vertex = self.vertices[vertex]
        path = []
        dist = vertex.dist[count]
        while vertex is not None:
            path.insert(0, vertex.id)
            vertex = vertex.ances[count]
        return (dist, path)

class diGraph(Graph):
    def addEdge(self, srcID, destID, weight):
        src = self.vertices[srcID]
        dest = self.vertices[destID]
        src.addEdge(Edge(src, dest, weight))

class Vertex(object):
    def __init__(self, ID):
        self.id = ID
        self.edges = []
        self.ances = [None, None]
        self.dist = [float('inf'), float('inf')]
        self.isCustomer = False
        self.index = None
        
    def addEdge(self, edge):
        self.edges.append(edge)
    
    def changeWeight(self, src, dest, weight):
        for edge in self.edges:
            if edge.src == src and edge.dest == dest:
                edge.weight = weight
                return 'Done'
        return 'Not Found'
    
    def isEdge(self, search):
        """
        returns (boolean, index)
        """
        for index, edge in enumerate(self.edges):
            if edge == search:
                return (True, index)
    
    def __eq__(self, other):
        return self.dist == other.dist 
    
    def __str__(self):
        return 'Vertex({0})'.format(self.id)
    
    def __repr__(self):
        return str(self)

    def __lt__(self, vertex):
        return self.dist[times] < vertex.dist[times]

    def __le__(self, vertex):
        return self.dist[times] <= vertex.dist[times]

    
class Edge(object):
    def __init__(self, src, dest, weight = 1):
        self.src = src
        self.dest = dest
        self.weight = weight
        
    def __eq__(self, other):
        return self.src == other.src and self.dest == other.dest and self.weight == other.weight
    
    def __str__(self):
        return str(self.src) + '<->' + str(self.dest)
    
    def __repr__(self):
        return str(self)
    
def loadGraph(fileName):
    """
    Sample of file:
    u v weight
    0 1 950
    0 2 3590
    1 3 3340
    2 5 1370
    """
    if '.txt' not in fileName:
        fileName += '.txt'
    file = open(fileName, 'r')
    maxID = 0 #just used to store temp
    for line in file:
        line = line.strip()
        line = line.split()
        if len(line) == 1:
            maxID = int(line[0])
            graph = Graph(maxID)
        else:
            """
            0 1 2
            u v weight
            """
            graph.addEdge(int(line[0]), int(line[1]), int(line[2]))
    file.close()
    return graph

def binarySearch(vertexList, vertexID):
    raise NotImplementedError

def getMaxID():
    return len(graph.vertices)

def getGraph():
    return graph

def findpath(src, dest, customer=False):
    if not customer:
        return solveTask1(graph, src, dest)
    else: 
        return solveTask2(graph, src, dest)

def solveTask1(graph, src, dest):
    global times
    times = 0
    graph.dijkstra(src, dest)
    dist, path = graph.getPath()
    return print_solution(path, dist, 1)
    
def solveTask2(graph, src, dest):
    """
    Don't need to reinitialise and dijsktra for the first time
    since task1 will do it already
    TODO: Change to use only one graph, make vertices have 2 variables
    """
    customers = get_customers('./path_finder/customers.txt')
    graph.insertCustomers(customers)
    dist, path = graph.getPath()
    for vertexID in path:
        if graph.vertices[vertexID].isCustomer:
            return print_solution(path, dist, 2)
    """
    first dijkstra + seocnd dijsktra path to include customers
    Prevents dupe id
    [] + [1:]
    """
    global times
    times = 1
    shortestPath = (float('inf'), src)
    graph.dijkstra(dest, src)
    for customer in customers:
        shortestPath = min((graph.vertices[customer].dist[0] + graph.vertices[customer].dist[1], customer), shortestPath)
    first = graph.getPath(shortestPath[1], 0)[1]
    second = graph.getPath(shortestPath[1], 1)[1]
    detourDist = shortestPath[0]
    detourPath = first + second[::-1][1:]
    return print_solution(detourPath, detourDist, 2)     

###################################################
# DO NOT MODIFY THE LINES IN THE BLOCK BELOW.
# YOU CAN WRITE YOUR CODE ABOVE OR BELOW THIS BLOCK
###################################################
def get_customers(filename):
    file = open(filename)
    customers = []
    for line in file:
        line = line.strip()
        customers.append(int(line))
    return customers

# path is a list of vertices on the path, distance is the total length of the path
# task_id must be 1 or 2 (corresponding to the task for which solution is being printed
def print_solution(path,distance,task_id):
    print()
    if task_id == 1:
        print("Shortest path: ", end ="")
    else:
        print("Minimum detour path: ",end="")

    customers = get_customers("./path_finder/customers.txt")
    
    vertices = []
    for item in path:
        if item in customers: 
            vertices.append(str(item)+ "(C)")
        else:
            vertices.append(str(item))

    path = " --> ".join(vertices)
    print(path)
    if task_id == 1:
        print("Shortest distance:", distance)
    else:
        print("Minimum detour distance:",distance)
    return path, distance

# source = int(input("Enter source vertex: "))
# target = int(input("Enter target vertex: "))
####################################################
# DO NOT MODIFY THE LINES IN THE ABOVE BLOCK.
# YOU CAN WRITE YOUR CODE ABOVE OR BELOW THIS BLOCK
###################################################
#source = [580, 947]#[220, 580, 947, 849, 315, 300, 315]
#target = [585, 1000]#[183, 585, 1000, 790, 255, 300, 315]
#for i in range(len(source)):
#    graph = loadGraph('edges.txt')
#    solveTask1(graph, source[i], target[i])
#    solveTask2(graph, source[i], target[i])
graph = loadGraph('./path_finder/edges.txt')
# solveTask1(graph, source, target)
# solveTask2(graph, source, target)