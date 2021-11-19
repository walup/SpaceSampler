import numpy as np
import random 
from scipy.stats import wasserstein_distance
import random
from DistanceType import DistanceType

class DistanceCalculator:

    def euclideanDistance(self, vector1, vector2):

        if(len(vector1) != len(vector2)):
            print("Los vectores deben ser del mismo tamaño")
            return -1

        n = len(vector1)
        distance = 0
        for i in range(0,n):
            distance = distance + (vector1[i] - vector2[i])**2

        return np.sqrt(distance)

    def wassersteinDistance(self, vector1, vector2):
        nSample = 500
        data1 = generateDataWithDistribution(vector1, nSample)
        data2 = generateDataWithDistribution(vector2, nSample)

        return wasserstein_distance(data1, data2)

    def aitchinsonDistance(self, vector1, vector2):
        if(len(vector1) != len(vector2)):
            print("Los vectores deben ser del mismo tamaño")
            return -1

        n = len(vector1)
        distance = 0
        for i in range(0,n):
            for j in range(i+1,n):
                xi = vector1[i]
                xiPrime = vector1[j]
                xj = vector2[i]
                xjPrime = vector2[j]
                if(xi != 0 and xiPrime != 0 and xj != 0 and xjPrime != 0):
                    distance = distance + (1/(n**2))*(np.log(xi/xiPrime) - np.log(xj/xjPrime))**2
        distance = np.sqrt(distance)
        return distance

    def computeDistance(self, vector1, vector2, distanceType):
        if(distanceType == DistanceType.EUCLIDEAN_DISTANCE):
            return self.euclideanDistance(vector1, vector2)
        elif(distanceType == DistanceType.WASSERSTEIN_DISTANCE):
            return self.wassersteinDistance(vector1, vector2)
        elif(distanceType == DistanceType.AITCHINSON_DISTANCE):
            return self.aitchinsonDistance(vector1, vector2)


def generateDataWithDistribution(distribution, nData):
    distribution = np.array(distribution)/sum(distribution)
    cumulativeDistribution = np.zeros(len(distribution) + 1)
    #Calculamos la distribución acumulada
    for i in range(1, len(cumulativeDistribution)):
        cumulativeDistribution[i] = cumulativeDistribution[i - 1] + distribution[i-1]

    generatedData = []
    for i in range(0,nData):
        diceRoll = random.random()
        index = 0
        for j in range(1, len(cumulativeDistribution)):
            if(diceRoll >= cumulativeDistribution[j-1] and diceRoll<= cumulativeDistribution[j]):
                index = j-1
                generatedData.append(index)
                break
    
    return generatedData





