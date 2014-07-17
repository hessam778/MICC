import numpy as np
from curves import fixMatrixSigns, boundaryCount, genus, ladderConvert, vectorSolution, distance, edges
from graph import Graph

class CurvePair:
    '''
    ladder = None
    beta = None
    top = []
    bottom = []
    n = 0
    matrix = None
    boundaries = None
    genus = None
    edges = None

    solution = None
    distance = 0
    loops = []
    '''
    def __init__(self,topBeta,bottomBeta, dist=1, graph=1):

        is_ladder = lambda top, bottom: not (0 in top or 0 in bottom)

        if is_ladder(topBeta,bottomBeta):
            self.ladder = [topBeta, bottomBeta]
        else:
            self.ladder = None
        


        if is_ladder(topBeta, bottomBeta):
            self.beta = ladderConvert(topBeta, bottomBeta)
            self.top = self.beta[0]
            self.bottom = self.beta[1]
        else:
            self.top = topBeta
            self.bottom = bottomBeta
            self.beta = [self.top, self.bottom]

        self.n = len(self.top)

        self.matrix = np.zeros((2,self.n,4))
        self.matrix[0,:,0] = [self.n-1] + range(self.n-1)
        self.matrix[0,:,1] = self.top
        self.matrix[0,:,2] = range(1,self.n) +[0]
        self.matrix[0,:,3] = self.bottom

        self.matrix = fixMatrixSigns(self.matrix)

        self.boundaries = boundaryCount(self.matrix)
        self.genus = genus(self.matrix)
        self.edges = edges(self.matrix)

        self.solution = vectorSolution(self.edges[0])


        if graph is 1:
            self.loops = Graph(self, self.edges).gammas
        else:
            self.loops = []

        if dist is 1:
            self.distance, self.loopMatrices = distance(self.matrix,self.loops)
        else:
            self.distance = None

        def __repr__(self):
            return self.ladder[0]+'\n'+self.ladder[1]+'\n'