# -*- coding: utf-8 -*-

""" Aluno: Leonardo Santos Paulucio
    Data: 06/05/19
    Trabalho 1 de Visão Computacional"""

# Standard libraries
import numpy as np

# My libraries
from Transforms import Transforms


class Object(Transforms):
    """ Object class
        This class inherits Transforms
    """

    def __init__(self, points=None):
        super().__init__(points)

    def loadFile(self, filename):
        points = np.loadtxt(filename).T
        self.setWorldPoints(np.vstack((points, np.ones(points.shape[1]))))
