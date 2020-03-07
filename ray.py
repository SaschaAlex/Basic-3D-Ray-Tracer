from vector import Vector3d,Vector
from math import sqrt

class Ray:
    def __init__(self,position : Vector, direction : Vector):
        self.dir = direction
        self.pos = position
    def point(self,scalar:float) -> Vector:
        return self.pos + scalar*self.dir
    def __repr__(self):
        return "{0} + t{1}".format(self.pos,self.dir)


class Plane :
    def __init__(self,position : Vector ,normal : Vector,width : float , heigth : float ,ncoef : float,
    color : tuple):
        self.pos    = position
        self.normal = normal
        self.color  = color
        self.ncoef  = ncoef
    def inter(self,Ray) -> float:
        pass
    def normal(self,point: Vector) -> Vector:
        return self.normal

class Sphere:
    def __init__(self, position : Vector, radius : float,nCoef : float,
        color : tuple):
        if 1 <= nCoef:
            self.nCoef  = nCoef
        else:
            raise Exception("The refraction coefficient cannot be less than 1")
        self.pos    = position
        self.radius = radius
        self.color  = color
    def inter(self,ray :object) -> float: # or None
        if type(ray) is Ray:
            a = ray.dir.dot(ray.dir)
            b = 2*(ray.pos - self.pos).dot(ray.dir)
            c = (ray.pos - self.pos).dot(ray.pos - self.pos)-self.radius**2
            delta = b**2 -4*a*c
            if delta >= 0:
                sqrt_detla = sqrt(delta)
                test = filter(lambda a: a > 0, [(-1*b+sqrt_detla)/(2*a),(-1*b-sqrt_detla)/(2*a)])
                if test == []:
                    return None
                else:
                    return min(test)
            else:
                return None
        else:
            raise Exception("This only works with ray !")
                
    def normal(self,point : Vector) -> Vector :
        norm = (point-self.pos).normalised()
        return norm

def reflected_ray(pos : Vector,normal : Vector,  Ri : object) -> Vector:
    return Ray(pos, Ri.dir - 2*(Ri.dir.dot(normal))*normal)

