from typing import List,Tuple
from functools import reduce
Grid2D = List[List[Tuple[int]]]


class PPM_RGB:
    """
    This class will create an image
    """
    def __init__(self,grid : Grid2D) -> None:
        isValid = lambda a : 0 <= a <= 255 and type(a) is int
        self.width = len(grid[0])
        self.height  = len(grid)
        if not all(map(lambda a : len(a) == self.width,grid)):
            raise Exception("Invalid grid dimension")
        for row in grid:
            for pixel in row:
                if not all(map(isValid,pixel)) and len(pixel) == 3:
                    raise Exception("The color is out of bound")
        self.image  = grid
    def encode(self,path) -> None:
        with open(path,"w") as f:
            f.write("P3\n{0} {1}\n255\n".format(self.width,self.height))
            for row in self.image:
                for pixel in row:
                    f.write("{0} {1} {2}\n".format(*pixel))

