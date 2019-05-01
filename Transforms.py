# Standard libraries
import numpy as np
from math import cos, sin


class Transforms:

    def __init__(self, points):
        self.points = points
        self.rotationMatrix = self.newRotationMatrix('z', 0)
        self.translationMatrix = self.newTranslationMatrix(0, 0, 0)
        self.baseMatrix = self.newBaseMatrix()

    def translate(self, dx=0, dy=0, dz=0):
        self.translationMatrix[0][-1] += dx
        self.translationMatrix[1][-1] += dy
        self.translationMatrix[2][-1] += dz
        self.points = np.dot(self.newTranslationMatrix(dx, dy, dz), self.points)

    def rotate(self, axis, angle):
        self.rotationMatrix = np.dot(self.newRotationMatrix(axis, angle), self.rotationMatrix)
        self.points = np.dot(self.newRotationMatrix(axis, angle), self.points)

    def rotateSelf(self, axis, angle):
        xc = np.mean(self.getWorldPoints()[0,:])
        yc = np.mean(self.getWorldPoints()[1,:])
        zc = np.mean(self.getWorldPoints()[2,:])
        self.baseMatrix = np.dot(self.newRotationMatrix(axis, angle)[0:-1, 0:-1], self.baseMatrix)
        m = np.dot(self.newRotationMatrix(axis, angle), self.newTranslationMatrix(-xc, -yc, -zc))
        m = np.dot(self.newTranslationMatrix(xc, yc, zc), m)
        self.setWorldPoints(np.dot(m, self.points))

    def getWorldPoints(self):
        return self.points

    def setWorldPoints(self, pts):
        self.points = pts

    def getRotationMatrix(self):
        return self.rotationMatrix

    def getTranslationMatrix(self):
        return self.translationMatrix

    def getBaseMatrix(self):
        return np.dot(self.getRotationMatrix()[0:-1, 0:-1], self.baseMatrix)

    def getExtrinsicMatrix(self):
        return np.dot(self.getRotationMatrix(), self.getTranslationMatrix())

    def getPoints3d(self):
        # return np.dot(self.getExtrinsicMatrix(), self.getWorldPoints())
        return self.points

    @staticmethod
    def newBaseMatrix():

        return np.array([[1, 0, 0],
                         [0, 1, 0],
                         [0, 0, 1]])

    @staticmethod
    def newProjectionMatrix():

        return np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0]])

    @staticmethod
    def newRotationMatrix(axis, angle):

        if axis == 'x':
            return np.array([[1,     0,            0,     0],
                             [0, cos(angle), -sin(angle), 0],
                             [0, sin(angle),  cos(angle), 0],
                             [0,     0,           0,      1]])

        elif axis == 'y':
            return np.array([[cos(angle),  0, sin(angle), 0],
                             [0,           1,      0,     0],
                             [-sin(angle), 0, cos(angle), 0],
                             [0,           0,      0,     1]])

        elif axis == 'z':
            return np.array([[cos(angle), -sin(angle), 0, 0],
                             [sin(angle),  cos(angle), 0, 0],
                             [0,               0,      1, 0],
                             [0,               0,      0, 1]])

    @staticmethod
    def newTranslationMatrix(dx, dy, dz):

        return np.array([[1, 0, 0, dx],
                         [0, 1, 0, dy],
                         [0, 0, 1, dz],
                         [0, 0, 0, 1]])

    @staticmethod
    def newScaleMatrix(sx, sy, sz):

        return np.array([[sx, 0, 0, 0],
                         [0, sy, 0, 0],
                         [0, 0, sz, 0],
                         [0, 0, 0, 1]])

    @staticmethod
    def set_axes_equal(axis):
        """ Make axes of 3D plot have equal scale so that spheres appear as spheres,
            cubes as cubes, etc..  This is one possible solution to Matplotlib's
            ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

            Input
            axis: a matplotlib axis, e.g., as output from plt.gca(). """

        x_limits = axis.get_xlim3d()
        y_limits = axis.get_ylim3d()
        z_limits = axis.get_zlim3d()

        x_range = abs(x_limits[1] - x_limits[0])
        x_middle = np.mean(x_limits)
        y_range = abs(y_limits[1] - y_limits[0])
        y_middle = np.mean(y_limits)
        z_range = abs(z_limits[1] - z_limits[0])
        z_middle = np.mean(z_limits)

        # The plot bounding box is a sphere in the sense of the infinity
        # norm, hence I call half the max range the plot radius.
        plot_radius = 0.5*max([x_range, y_range, z_range])

        axis.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
        axis.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
        axis.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])
