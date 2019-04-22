# Standard libraries
import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin


class Transforms:

    def __init__(self, points):
        self.points = points
        self.rotationMatrix = self.newRotationMatrix('z', 0)
        self.translationMatrix = self.newTranslationMatrix(0, 0, 0)

    def translate(self, dx=0, dy=0, dz=0):
        self.translationMatrix[0][-1] += dx
        self.translationMatrix[1][-1] += dy
        self.translationMatrix[2][-1] += dz

    def rotate(self, axis, angle):
        self.rotationMatrix = np.dot(self.rotationMatrix, self.newRotationMatrix(axis, angle))

    def getWorldPoints(self):
        return self.points

    def setWorldPoints(self, pts):
        self.points = pts

    def getRotationMatrix(self):
        return self.rotationMatrix

    def getTranslationMatrix(self):
        return self.translationMatrix

    def getExtrinsicMatrix(self):
        m = self.getRotationMatrix()
        m[0][-1] = self.translationMatrix[0][-1]
        m[1][-1] = self.translationMatrix[1][-1]
        m[2][-1] = self.translationMatrix[2][-1]
        return m

    def getPoints3d(self):
        return np.dot(self.getExtrinsicMatrix(), self.getWorldPoints())

    @staticmethod
    def newBaseMatrix():

        return np.array([[1, 0, 0]
                         [0, 1, 0]
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


if __name__ == "__main__":

    obj = loadObject('box.xyz')

    fig = plt.figure()
    ax0 = fig.add_subplot(5, 1, 1)
    ax0 = plt.axes(projection='3d')
    ax0.set_title('3D points')
    ax0.set_xlabel('x-axis')
    ax0.set_ylabel('y-axis')
    ax0.set_zlabel('z-axis')
    ax0.set_xlim([-2, 2])
    ax0.set_ylim([-1, 1])
    ax0.set_zlim([4, 8])

    ax0.plot3D(obj[0, :], obj[1, :], obj[2, :], 'k.')
    ax0.view_init(elev=25, azim=-65)
    # plt.show()
