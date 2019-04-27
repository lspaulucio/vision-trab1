# Standard libraries
import numpy as np
import matplotlib.pyplot as plt
from stl import mesh
from mpl_toolkits.mplot3d import art3d

# My libraries
from Transforms import Transforms


class Object(Transforms):
    """ Object class
        This class inherits Transforms
    """

    def __init__(self, points=None):
        super().__init__(points)
        self.mesh = None
        self.vectors = None
        self.stl = False

    def isSTL(self):
        return self.stl

    def loadFile(self, filename):
        self.stl = False
        points = np.loadtxt(filename).T
        self.setWorldPoints(np.vstack((points, np.ones(points.shape[1]))))

    def loadSTL(self, filename):
        self.stl = True
        your_mesh = mesh.Mesh.from_file(filename)
        # Get the x, y, z coordinates contained in the mesh structure that are the
        # vertices of the triangular faces of the object
        x = your_mesh.x.flatten()
        y = your_mesh.y.flatten()
        z = your_mesh.z.flatten()

        # Create the 3D object from the x,y,z coordinates and add the additional array of ones to
        # represent the object using homogeneous coordinates
        self.points = np.array([x.T,y.T,z.T,np.ones(x.size)])

        # Get the vectors that define the triangular faces that form the 3D object
        self.vectors = your_mesh.vectors

        # print(self.vectors[0])
        #print(kong.shape)

    def showSTL(self):
        ###################################################
        # Plotting the 3D vertices of the triangular faces
        ###################################################

        # Create a new plot
        # fig = plt.figure(1)
        # axes0 = plt.axes(projection='3d')

        # Plot the points drawing the lines
        # points = self.points
        # axes0.plot(points[0,:], points[1,:], points[2,:],'r')
        # Transforms.set_axes_equal(axes0)
        # plt.show()

        ###################################################
        # Plotting the 3D triangular faces of the object
        ###################################################
        # Create a new plot
        plt.figure(2)
        axes1 = plt.axes(projection='3d')
        points = self.points
        # Plot and render the faces of the object
        axes1.add_collection3d(art3d.Poly3DCollection(self.vectors))
        # Plot the contours of the faces of the object
        axes1.add_collection3d(art3d.Line3DCollection(self.vectors, color='k', linewidths=0.2, linestyles='-'))
        # Plot the vertices of the object
        # axes1.plot(kong[0,:],kong[1,:],kong[2,:],'k.')

        # Set axes and their aspect
        axes1.auto_scale_xyz(points[0,:], points[1,:], points[2,:])
        Transforms.set_axes_equal(axes1)
        # Show the plots
        plt.show()
