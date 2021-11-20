import numpy as np
from DistanceCalculator import DistanceCalculator
import matplotlib.pyplot as plt
from DistanceType import DistanceType
import random

class SimplexSpaceSampler:

    #Muestreo aleatorio de una bola
    def sampleBallPoints(self, center, radius, nPoints, distanceType):
        nDimensions = len(center)
        center = np.array(center)
        center = center/sum(center)
        points = []
        index = 0
        distanceCalculator = DistanceCalculator()
        maxIterations = 100*nPoints
        cycleCount = 0
        while(index < nPoints or cycleCount > maxIterations):
            #Vamos a muestrear dentro de un cuadrado centrado en center y con lado igual a 2r, 
            #Esto supongo va a ser un tanto lento, sobre todo si quisieramos muestrear muchos
            #puntos, pero como las geometrías son demasiado generales no veo otra forma realmente
            newPoint = []
            for j in range(0,nDimensions):
                newPoint.append((center[j]-radius) + 2*random.random()*radius)
            
            newPoint = np.array(newPoint)
            newPoint = newPoint/sum(newPoint)

            if(distanceCalculator.computeDistance(newPoint, center, distanceType) <= radius):
                points.append(newPoint)
                index += 1
            cycleCount += 1

        return np.array(points)

    #Muestreo aleatorio de un anillo
    def sampleAnnulusPoints(self, center, radius1, radius2, nPoints, distanceType):
        nDimensions = len(center)
        center = np.array(center)
        center = center/sum(center)
        points = []
        index = 0
        distanceCalculator = DistanceCalculator()
        maxIterations = 100*nPoints
        cycleCount = 0
        while(index < nPoints or cycleCount > maxIterations):
            newPoint = []
            for j in range(0,nDimensions):
                newPoint.append((center[j] - radius2) + 2*random.random()*radius2)
            newPoint = np.array(newPoint)
            newPoint = newPoint/sum(newPoint)
            dist = distanceCalculator.computeDistance(newPoint, center, distanceType)
            if(dist >=  radius1 and dist<= radius2):
                points.append(newPoint)
                index += 1
            
            cycleCount += 1

        return np.array(points)

    #Este lo voy a ver como un caso particular del anillo
    def samplePerimeterPoints(self, center, radius, nPoints, distanceType, epsilon = 0.1):
        radius1 = radius - epsilon
        radius2 = radius + epsilon
        return self.sampleAnnulusPoints(center, radius1, radius2, nPoints, distanceType)
    
    
    
    def sampleSimplexPointsOutsideCircle(self, center, radius, nPoints, distanceType):
        nDimensions = len(center)
        center = np.array(center)
        center = center/sum(center)
        points = []
        index = 0
        distanceCalculator = DistanceCalculator()
        maxIterations = 100*nPoints
        cycleCount = 0
        while(index < nPoints or cycleCount > maxIterations):
            #Vamos a muestrear dentro de un cuadrado centrado en center y con lado igual a 2r, 
            #Esto supongo va a ser un tanto lento, sobre todo si quisieramos muestrear muchos
            #puntos, pero como las geometrías son demasiado generales no veo otra forma realmente
            newPoint = []
            for j in range(0,nDimensions):
                newPoint.append(random.random())
            
            newPoint = np.array(newPoint)
            newPoint = newPoint/sum(newPoint)

            if(distanceCalculator.computeDistance(newPoint, center, distanceType) >= radius):
                points.append(newPoint)
                index += 1
            cycleCount += 1

        return np.array(points)
    
    
    def sampleSimplexPointsOutsideAnnulus(self, center, radius1, radius2, nPoints, distanceType):
        nDimensions = len(center)
        center = np.array(center)
        center = center/sum(center)
        points = []
        index = 0
        distanceCalculator = DistanceCalculator()
        maxIterations = 100*nPoints
        cycleCount = 0
        while(index < nPoints or cycleCount > maxIterations):
            newPoint = []
            for j in range(0,nDimensions):
                newPoint.append(random.random())
            newPoint = np.array(newPoint)
            newPoint = newPoint/sum(newPoint)
            dist = distanceCalculator.computeDistance(newPoint, center, distanceType)
            if(dist <=  radius1 or dist >= radius2):
                points.append(newPoint)
                index += 1
            
            cycleCount += 1

        return np.array(points)
    
    
    def sampleSimplexPointsOutsidePerimeter(self, center, radius, nPoints, distanceType, epsilon = 0.1):
        radius1 = radius - epsilon
        radius2 = radius + epsilon
        return self.sampleSimplexPointsOutsideAnnulus(center, radius1, radius2, nPoints, distanceType)




