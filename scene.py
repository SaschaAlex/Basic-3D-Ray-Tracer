from vector import Vector3d,Vector
from ray    import Sphere,Ray,reflected_ray
from PPM    import PPM_RGB

class Camera:
    def __init__(self,pos : Vector,dire : Vector, hvector : Vector,
     heigth : int , width : int,pixelsize : float):
        self.pos    = pos 
        self.dire = dire
        self.heigth = heigth
        self.width  = width
        self.pixelsize = pixelsize
        self.dh = -1*pixelsize*hvector.normalised()
        self.dw = pixelsize*self.dire.cross(self.dh).normalised()
        self.center = (width//2,heigth//2)
    def pixelToWord(self,i:int,j:int) -> Vector:
        if  0 <= i < self.heigth and 0 <= j < self.width:
            l1 , l2 = self.center[0] - i , self.center[1] - j
            return Ray(self.pos,(l1 * self.dh + l2 * self.dw + self.dire))
        else:
            raise Exception("Index out of range!")
        
    def traceImage(self,scene : object) -> list:
        I = [[0 for k in range(self.width)] for i in range(self.heigth)]
        for i,row in enumerate(I):
            for j,_ in enumerate(row):
                ray = self.pixelToWord(*(i,j))
                color,ob,dist = self.traceRay(scene,ray)
                Id = self.diffuse(ray,ob,scene.light,dist) # diffusion
                IS = self.specular(ray,ob,dist)
                I[i][j] = self.add(color,IS,Id,scene.ka)
                #I[i][j] = self.add((0,0,0),IS,Id,scene.ka)
        return I
    def diffuse(self,ray : object,ob : object, lights : object ,t : float,kd=300):
        if type(ray) is Ray:
            if ob == None : return 0.0
            hold = 0
            for light in lights.values():
                point  = ray.point(t) # vector
                sourceL= (light.pos-point).normalised() # vector
                normal = ob.normal(point) # Vector
                hold += normal.dot(sourceL)
            return kd*hold

        else:
            raise Exception("Invalid type")
    def specular(self,ray : object, ob : object,t : float, ks=0.15, n = 250):
        if type(ray) is Ray:
            if ob == None : return 0.0
            pos    = ray.point(t)
            V      =  ray
            normal = ob.normal(pos)
            R = reflected_ray(pos,normal,ray)
            #return 0 
            return ks * (-1*R.dir.normalised().dot(V.dir.normalised()))**n
    
    def add(self,ambian : float,specular : float , diffuse : float,ka : float) -> float:
        hold   = map(lambda I : int(specular + diffuse+ka*I), ambian)
        boundU = map(lambda I : 255 if I >= 255 else I,hold)
        boundL = map(lambda I : 0   if I <= 0  else I,boundU)

        return tuple(boundL)

    def traceRay(self,scene : object, ray : object) -> tuple:
        ob,dist = scene.closedInter(ray)
        if ob == None : return ((0,0,0),None,None)
        else: return (ob.color,ob,dist)

    def rendering(self,scene : object):
        Grid  = self.traceImage(scene)
        Image = PPM_RGB(Grid)
        Image.encode("./test.ppm")
       
        
        
class Light:
    def __init__(self,pos : Vector):
        self.pos = pos

class Scene:
    def __init__(self,name: str,ka : float):
        self.ka  = ka
        self.name   = name
        self.object = {}
        self.camera = {}
        self.light  = {}
    def addObject(self,name : str,ob : object) -> None:
        self.object.update({"{0}".format(name): ob})
    def delObject(self,name : str) -> None:
        self.object.pop(name)
    def addCamera(self,name : str,ob : object) -> None:
        self.camera.update({"{0}".format(name): ob})
    def delCamera(self,name : str) -> None:
        self.camera.pop(name)
    def addLight(self,name : str,ob : object) -> None:
        self.light.update({"{0}".format(name): ob})
    def delLight(self,name : str) -> None:
        self.light.pop(name)
    def closedInter(self,ray : object) -> tuple:
        """
        return (object,distance)
        """
        c_ob  = None
        c_dis = 999999999999999999999
        for (key , ob) in self.object.items():
            distance = self.object[key].inter(ray) # all distance is Nome
            if distance != None:
                if c_dis > distance:
                    c_dis,c_ob = distance,ob
        return (c_ob,c_dis)


#Test

print("fooo")

camera = Camera(Vector3d(0,0,0),Vector3d(1,0,0),Vector3d(0,1,0),500,500,0.01)
sphere = Sphere(Vector3d(10,0,0),7,1,(79,232,210))
light  = Light(Vector3d(-10,0,-200))

ray = Ray(Vector3d(0,0,0),Vector3d(*[1.0, 0.84, -0.6]))
print("The intial ray is from {0}".format(ray))

print(f"{camera.pixelToWord(0,0)}")
print(f"{camera.pixelToWord(0,99)}")
print(f"{camera.pixelToWord(99,0)}")
print(f"{camera.pixelToWord(99,99)}")

scene = Scene("test",0.5)
scene.addObject("s1",sphere)
scene.addCamera("c1",camera)
scene.addLight("L1" ,light)

camera.rendering(scene)



