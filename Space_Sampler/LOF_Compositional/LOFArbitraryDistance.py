from DistanceCalculator import DistanceCalculator
import numpy as np
from tqdm import tqdm

class LOFArbitraryDistance:
    
    def __init__(self, data, distanceType, minPoints):
        """
        data: una tabla de datos donde cada fila es un vector
        """
        self.minPoints = minPoints
        nData = np.size(data, 0)
        distanceCalculator = DistanceCalculator()
        distanceMatrix = np.zeros((nData, nData))
        print("Obteniendo matriz de distancias")
        for i in range(0,nData):
            if((i/nData)*100 % 10 < 0.05):
                print(str(round((i/nData)*100)) + " % completado ")
            point1 = data[i,:]
            for j in range(i+1, nData):
                point2 = data[j,:]
                dst = distanceCalculator.computeDistance(distanceType, point1, point2)
                distanceMatrix[i,j] = dst
                #Symmetry of distance
                distanceMatrix[j,i] = dst
        self.distanceMatrix = distanceMatrix
    
    def getKDistance(self, pointIndex):
        foundVectors = []
        distanceVector = list(np.sort(self.distanceMatrix[pointIndex, :]))
        return distanceVector[self.minPoints]
    #Para usar este metodo hay que obtener primero la distancia k
    def getNeighborhood(self, pointIndex, kDistance):
        neighborIndexes = []
        distanceVector = self.distanceMatrix[pointIndex, :]
        for i in range(0,np.size(self.distanceMatrix,0)):
            if(distanceVector[i] <= kDistance):
                neighborIndexes.append(i)
        
        return neighborIndexes
    
    def getReachabilityDistance(self, pointIndex, neighborIndex):
        d = self.distanceMatrix[pointIndex, neighborIndex]
        kDistance = self.getKDistance(neighborIndex)
        return np.max([d, kDistance])
    
    def getLocalReachabilityDistance(self, pointIndex):
        pointKDistance = self.getKDistance(pointIndex)
        #Obtenemos los puntos del k-vecindario
        neighbors = self.getNeighborhood(pointIndex, pointKDistance)
        nNeighbors = len(neighbors)
        lrd = 0
        for i in range(0,nNeighbors):
            neighborIndex = neighbors[i]
            reachDist = self.getReachabilityDistance(pointIndex, neighborIndex)
            lrd = lrd + reachDist/nNeighbors
        lrd = 1/lrd
        return lrd
    
    
    def getLOFScore(self, pointIndex):
        lrdPoint = self.getLocalReachabilityDistance(pointIndex)
        pointKDistance = self.getKDistance(pointIndex)
        neighbors = self.getNeighborhood(pointIndex, pointKDistance)
        nNeighbors = len(neighbors)
        lofScore = 0
        for i in range(0,nNeighbors):
            neighborIndex = neighbors[i]
            lrdNeighbor = self.getLocalReachabilityDistance(neighborIndex)
            lofScore = lofScore + lrdNeighbor/lrdPoint
        
        return lofScore/nNeighbors
    
    def computeAllLOFScores(self):
        lofScores = []
        nData = np.size(self.distanceMatrix,0)
        for i in tqdm(range(0,nData)):
            lofScores.append(self.getLOFScore(i))
        return lofScores    