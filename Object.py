# -*- coding: utf-8 -*-

""" Aluno: Leonardo Santos Paulucio
    Data: 06/05/19
    Trabalho 1 de Visão Computacional"""

# Standard libraries
import numpy as np
from stl import mesh
import copy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import art3d


# My libraries
from Transforms import Transforms


class Object(Transforms):
    """ Object class
        This class inherits Transforms
    """

    def __init__(self, points=None):
        super().__init__(points)
        self.stl = False
        self.mesh = None

    def loadFile(self, filename):
        self.stl = False
        points = np.loadtxt(filename).T
        self.setWorldPoints(np.vstack((points, np.ones(points.shape[1]))))

    def isSTL(self):
        return self.stl

    def loadSTL(self, filename):
        self.stl = True
        self.mesh = mesh.Mesh.from_file(filename)
        # Get the x, y, z coordinates contained in the mesh structure that are the
        # vertices of the triangular faces of the object
        x = self.mesh.x.flatten()
        y = self.mesh.y.flatten()
        z = self.mesh.z.flatten()

        # Create the 3D object from the x,y,z coordinates and add the additional array of ones to
        # represent the object using homogeneous coordinates
        kong = np.array([x.T,y.T,z.T,np.ones(x.size)])
        self.setWorldPoints(kong)

    def showSTL(self):
        # Get the x, y, z coordinates contained in the mesh structure that are the
        # vertices of the triangular faces of the object
        x = self.mesh.x.flatten()
        y = self.mesh.y.flatten()
        z = self.mesh.z.flatten()

        obj_mesh = copy.deepcopy(self.mesh)
        obj_mesh.transform(Transforms.newRotationMatrix('z', 90/180*3.14))
        # Get the vectors that define the triangular faces that form the 3D object
        kong_vectors = obj_mesh.vectors

        # Create the 3D object from the x,y,z coordinates and add the additional array of ones to
        # represent the object using homogeneous coordinates
        kong = np.array([x.T,y.T,z.T,np.ones(x.size)])

        fig = plt.figure(2)
        axes1 = plt.axes(projection='3d')
        # Plot and render the faces of the object
        axes1.add_collection3d(art3d.Poly3DCollection(kong_vectors))
        # Plot the contours of the faces of the object
        axes1.add_collection3d(art3d.Line3DCollection(kong_vectors, colors='k', linewidths=0.2, linestyles='-'))
        # Plot the vertices of the object
        axes1.plot(kong[0,:],kong[1,:],kong[2,:],'k.')

        # Set axes and their aspect
        axes1.auto_scale_xyz(kong[0,:],kong[1,:],kong[2,:])
        Transforms.set_axes_equal(axes1)
        # Show the plots
        plt.show()


if __name__ == "__main__":
    obj = Object()
    obj.loadSTL("models/donkey_kong.STL")
    # obj.mesh.transform(Transforms.newRotationMatrix('z', 90/180*3.14))
    obj.showSTL()
    g = input()
    obj.showSTL()
