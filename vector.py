from math import sqrt
from typing import List

Vector = List[float]

class Vector3d:
    """
    These vectors are all in cartesian coordinate in R^3
    """
    def __init__(self,x : float , y : float, z : float):
        self.vector = [x,y,z]
    def __add__(self,other) -> Vector:
        if type(other) is Vector3d:
            return Vector3d(*[i+j for (i,j) in zip(self.vector,other.vector)])
        else:
            raise TypeError("You can only add 3d vector with 3d vector")
    def __sub__(self,other) -> Vector:
        if type(other) is Vector3d:
            return Vector3d(*[i-j for (i,j) in zip(self.vector,other.vector)])
        else:
            raise TypeError("You can only substract 3d vector with 3d vector")
    def __mul__(self,scalar) -> Vector:
        return scalar * self
    def __rmul__(self,scalar) -> Vector:
        if type(scalar) in [int,float]:
            return Vector3d(*map(lambda i : i * scalar, self.vector))
        else:
            raise TypeError("The scalar can only be int or float")
    def __truediv__(self,scalar):
        if type(scalar) in [int,float]:
            return Vector3d(*map(lambda i : i / scalar, self.vector))
        else:
            raise TypeError("The scalar can only be int or float")
    def __str__(self) -> str:
        return str(self.vector)
    def __repr__(self) -> str:
        return str(self.vector)
    def norm(self) -> float:
        return sqrt(sum([c*c for c in self.vector])) 
    def dot(self,other) -> float:
        if type(other) is Vector3d:
            return sum([x*y for (x,y) in zip(self.vector,other.vector)])
        else:
            raise TypeError("You can only dot 3d vector with 3d vector")
    def normalised(self) -> Vector:
       return Vector3d(*map(lambda i : i /self.norm(), self.vector))
    def cross(self,other) -> Vector:
        if type(other) is Vector3d:
            fst = self.vector[1]*other.vector[2]-self.vector[2]*other.vector[1] 
            snd = self.vector[0]*other.vector[2]-self.vector[2]*other.vector[0]
            trd = self.vector[0]*other.vector[1]-self.vector[1]*other.vector[0]
            return Vector3d(fst,-1*snd,trd)
        else:
            raise TypeError("You can only croos productuct 3d vector with 3d vector")
    
