# Standard libraries
import numpy as np
import matplotlib.pyplot as plt

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

    def loadFile(self, filename):
        self.stl = False
        points = np.loadtxt(filename).T
        self.setWorldPoints(np.vstack((points, np.ones(points.shape[1]))))

    # def loadSTL(self, filename):
    #     self.stl = True
    #     your_mesh = mesh.Mesh.from_file(filename)
    #     # Get the x, y, z coordinates contained in the mesh structure that are the
    #     # vertices of the triangular faces of the object
    #     x = your_mesh.x.flatten()
    #     y = your_mesh.y.flatten()
    #     z = your_mesh.z.flatten()
    #
    #     # Get the vectors that define the triangular faces that form the 3D object
    #     kong_vectors = your_mesh.vectors
    #
    #     # Create the 3D object from the x,y,z coordinates and add the additional array of ones to
    #     # represent the object using homogeneous coordinates
    #     kong = np.array([x.T,y.T,z.T,np.ones(x.size)])
    #
    #
    #     #print(kong.shape)
    #
    #     ###################################################
    #     # Plotting the 3D vertices of the triangular faces
    #     ###################################################
    #
    #     # Create a new plot
    #     fig = plt.figure(1)
    #     axes0 = plt.axes(projection='3d')
    #
    #     # Plot the points drawing the lines
    #     axes0.plot(kong[0,:],kong[1,:],kong[2,:],'r')
    #     set_axes_equal(axes0)
    #
    #     ###################################################
    #     # Plotting the 3D triangular faces of the object
    #     ###################################################
    #
    #     # Create a new plot
    #     fig = plt.figure(2)
    #     axes1 = plt.axes(projection='3d')
    #
    #     # Plot and render the faces of the object
    #     axes1.add_collection3d(art3d.Poly3DCollection(kong_vectors))
    #     # Plot the contours of the faces of the object
    #     axes1.add_collection3d(art3d.Line3DCollection(kong_vectors, colors='k', linewidths=0.2, linestyles='-'))
    #     # Plot the vertices of the object
    #     #axes1.plot(kong[0,:],kong[1,:],kong[2,:],'k.')
    #
    #     # Set axes and their aspect
    #     axes1.auto_scale_xyz(kong[0,:],kong[1,:],kong[2,:])
    #     set_axes_equal(axes1)
    #     # Show the plots
    #     plt.show()

    def show2d(self, m):

        # fig = plt.figure()
        # ax0 = fig.add_subplot(2, 1, 1)
        # print (self.points.shape, self.translationMatrix.shape, self.rotationMatrix.shape)
        v = self.getExtrinsicMatrix()
        v = np.dot(v, self.points)
        v = np.dot(Transforms.newProjectionMatrix(), v)
        v = np.dot(m.getIntrinsicMatrix(), v)
        plt.plot(v[0], v[1], 'g.')
        plt.show()

    def show3d(self):

        # ax0 = fig.add_subplot(2, 1, 2, projection='3d')
        points = self.getPoints3d()
        ax0 = plt.figure()
        ax0 = plt.axes(projection='3d')
        ax0.set_title('3D points')
        ax0.set_xlabel('x-axis')
        ax0.set_ylabel('y-axis')
        ax0.set_zlabel('z-axis')
        ax0.set_xlim([-2, 2])
        ax0.set_ylim([-1, 1])
        ax0.set_zlim([4, 8])
        ax0.plot3D(points[0, :], points[1, :], points[2, :], 'k.')
        ax0.view_init(elev=25, azim=-65)
        Transforms.set_axes_equal(ax0)
        plt.show()
