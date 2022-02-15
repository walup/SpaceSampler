import numpy as np
import random 
from scipy.stats import wasserstein_distance
import random
from DistanceType import DistanceType

class DistanceCalculator:
    """
    Clase utilizada para calcular las distancias
    """
    def manhattanDistance(self, vector1, vector2):
        n1 = len(vector1)
        n2 = len(vector2)
        #Si los vectores no son de igual dimensión vamos a mandar un 
        #mensaje al usuario
        if(n1 != n2):
            print("Los vectores deben ser de la misma dimensión")
            return -1
        d = 0
        for i in range(0,n1):
            d += np.abs(vector1[i] - vector2[i])
    
        return d


    def euclideanDistance(self, vector1, vector2):
        n1 = len(vector1)
        n2 = len(vector2)
    
        if(n1 != n2):
            print("Los vectores deben ser de la misma dimensión")
            return -1
    
        d = 0
        for i in range(0,n1):
            d += (vector1[i] - vector2[i])**2
    
        d = np.sqrt(d)
        return d


    def cosineDistance(self, vector1, vector2):
        n1 = len(vector1)
        n2 = len(vector2)
    
        if(n1 != n2):
            print("Los vectores deben ser de la misma dimensión")
            return -1
    
        #Obtenemos el producto punto y las dos normas
        dotProduct = 0
        norm1 = 0
        norm2 = 0
        for i in range(0,n1):
            dotProduct += vector1[i]*vector2[i]
            norm1 += vector1[i]**2
            norm2 += vector2[i]**2
    
        norm1 = np.sqrt(norm1)
        norm2 = np.sqrt(norm2)
    
        cosineDistance = 1 - (dotProduct/(norm1*norm2))
        return cosineDistance
    
    #Metodos necesarios para calcular la distancia Wasserstein
    def generateDataWithDistribution(self,distribution, nData):
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
    
    def wassersteinDistance(self, vector1, vector2):
        nGeneratedData = len(vector1)*10
        data1 = self.generateDataWithDistribution(vector1, nGeneratedData)
        data2 = self.generateDataWithDistribution(vector2, nGeneratedData)
        dst = wasserstein_distance(data1, data2)
        return dst
    
    
    def aitchisonDistance(self, vector1, vector2):
        #Debemos volver composicionales los datos p
        vector1 = np.array(vector1)/sum(vector1)
        vector2 = np.array(vector2)/sum(vector2)
        D = len(vector1)
        distance = 0
        for i in range(0,D):
            x1i = vector1[i]
            x2i = vector2[i]
            for j in range(0,D):
                x1j = vector1[j]
                x2j = vector2[j]
                if(x1i != 0 and x2i != 0 and x1j != 0 and x2j != 0):
                    distance = distance + (1/(2*D))*(np.log(x1i/x1j) - np.log(x2i/x2j))**2
        
        distance = np.sqrt(distance)
        
        return distance
                
        
    
    
    def computeDistance(self, distanceType, vector1, vector2):
        if(distanceType == DistanceType.MANHATTAN):
            return self.manhattanDistance(vector1, vector2)
        elif(distanceType == DistanceType.EUCLIDEAN):
            return self.euclideanDistance(vector1, vector2)
        elif(distanceType == DistanceType.WASSERSTEIN):
            return self.wassersteinDistance(vector1, vector2)
        elif(distanceType == DistanceType.COSINE):
            return self.cosineDistance(vector1, vector2)
        elif(distanceType == DistanceType.AITCHISON):
            return self.aitchisonDistance(vector1, vector2)