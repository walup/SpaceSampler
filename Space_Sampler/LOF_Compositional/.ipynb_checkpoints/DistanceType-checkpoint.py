from enum import Enum

class DistanceType(Enum):
    """
    Tipos de distancia a utilizar
    1.- Manhattan
    2.- Euclidiana
    3.- Wasserstein
    4.- Coseno
    5.- Aitchison (para datos composicionales)
    """
    MANHATTAN = 0
    EUCLIDEAN = 1
    WASSERSTEIN = 2
    COSINE = 3
    AITCHISON = 4
    