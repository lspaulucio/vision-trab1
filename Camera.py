# Standard libraries
import numpy as np

# My libraries
from Transforms import Transforms


class Camera(Transforms):
    """ Camera class
        This class inherits Transforms
    """

    def __init__(self):
        super().__init__(np.array([[0], [0], [0], [1]]))
        self.f = 1
        self.sx = 1
        self.sy = 1
        self.so = 0
        self.ox = 0
        self.oy = 0

    def setFocalDistance(self, d):
        self.f = d

    def setOx(self, x):
        self.ox = x

    def setOy(self, y):
        self.oy = y

    def setSx(self, x):
        self.sx = x

    def setSy(self, y):
        self.sy = y

    def getIntrinsicMatrix(self):
        return np.array([[self.f*self.sx, self.f*self.so, self.ox],
                         [0,              self.f*self.sy, self.oy],
                         [0,                     0,             1]])
