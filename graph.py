class Graph:
    def __init__(self,graph_dict={}):
        self.graph = graph_dict

    def inGraph(self,node,verbose=False):
        if verbose:
            if node in self.graph:
                print(str(node)," in graph")
            else:
                print(str(node)," not in graph")

        return node in self.graph

    def addNode(self,node):
        if node not in self.graph:
            self.graph[node] = []
        else:
            print("Node already in graph")

    def listNodes(self):
        print(self.graph.keys())
        return self.graph.keys()

    def addEdge(self,node1,node2):
        try:
            if node2 not in self.graph[node1]:
                self.graph[node1].append(node2)
            if node1 not in self.graph[node2]:
                self.graph[node2].append(node1)
        except KeyError:
            self.inGraph(node1,verbose=True)
            self.inGraph(node2,verbose=True)

    def deleteEdge(self,node1,node2):
        try:
            if node2 in self.graph[node1]:
                self.graph[node1].remove(node2)
            if node1 in self.graph[node2]:
                self.graph[node2].remove(node1)
        except KeyError:
            self.inGraph(node1,verbose=True)
            self.inGraph(node2,verbose=True)

    def deleteNode(self,node):
        try:
            for connectedNode in self.graph[node]:
                self.deleteEdge(node,connectedNode)
            del self.graph[node]
        except KeyError:
            self.inGraph(node,verbose=True)

    def areAdjacent(self,node1,node2):
        try:
            if node1 in self.graph[node2] and node2 in self.graph[node1]:
                #print("Nodes ",node1," and",node2," are neighbours")
                return True
            else:
                #print("Nodes ",node1," and",node2," are not neighbours")
                return False
        except KeyError:
            self.inGraph(node1,verbose=False)
            self.inGraph(node2,verbose=False)

    def BreadthFirstSearch(self,node):
        try:
            self.graph[node]
        except KeyError:
            ("Node doesn't exist")

        visited = {node}
        queue = [node]

        while len(queue)!=0:
            nextNode = queue.pop()
            for neighbour in self.graph[nextNode]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)

        #print("Visited the following nodes: ", visited)
        return visited

    def arePathConnected(self,node1,node2):
        allConnectedNodes = self.BreadthFirstSearch(node1)

        if node2 in allConnectedNodes:
            #print("Nodes ",node1," and",node2," are path connected")
            return True
        else:
            #print("Nodes ",node1," and",node2," are not path connected")
            return False
