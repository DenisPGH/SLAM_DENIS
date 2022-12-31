class EdgeRotation:
    """
    Class for choose the shortest way, between two angles in degrees
    """
    def __init__(self,source,destination,weight=45,direction=None):
        self.source = source
        self.destination = destination
        self.weight = weight
        self.direction=direction

# graph={}
# directions=['up','up-right','right','down-right','down','down-left','left','up-left']

class Rotation:
    def __init__(self):
        self.graph={}
        self.directions=[x for x in range(361)]

    def rot_graph(self):
        """
        crete a graph with 360 nodes, 360 degrees
        :return:
        """
        for dir in range(len(self.directions)):
            if  self.directions[dir] not in self.graph:
                self.graph[self.directions[dir]] = {}

            if dir<len(self.directions)-1:
                if self.directions[dir+1] not in self.graph:
                    self.graph[self.directions[dir + 1]] = {}

                self.graph[self.directions[dir]][f"{self.directions[dir]}-{self.directions[dir+1]}"]=(EdgeRotation(self.directions[dir],self.directions[dir+1],1,'R'))
                self.graph[self.directions[dir+1]][f"{self.directions[dir+1]}-{self.directions[dir]}"]=(EdgeRotation(self.directions[dir+1],self.directions[dir],1,'L'))
            else:
                self.graph[self.directions[dir]][f"{self.directions[dir]}-{self.directions[0]}"]=(EdgeRotation(self.directions[dir], self.directions[0],1,'R'))
                self.graph[self.directions[0]][f"{self.directions[0]}-{self.directions[dir]}"]=(EdgeRotation(self.directions[0], self.directions[dir],1,'L'))

        return self.graph


# a=Rotation()
# print(a.rot_graph())
# print()


