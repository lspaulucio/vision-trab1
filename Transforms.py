# -*- coding: utf-8 -*-

""" Aluno: Leonardo Santos Paulucio
    Data: 06/05/19
    Trabalho 1 de Visão Computacional"""

# Standard libraries
import numpy as np
from math import cos, sin
import matplotlib.pyplot as plt


class Transforms:
    """Class of 3d transforms"""

    def __init__(self, points):
        self.points = points
        self.extrinsicMatrix = self.newRotationMatrix('z', 0)

    def translate(self, dx=0, dy=0, dz=0):
        self.extrinsicMatrix = np.dot(self.newTranslationMatrix(dx, dy, dz), self.extrinsicMatrix)

    def translateOwnAxis(self, dx=0, dy=0, dz=0):
        vt = np.dot(self.extrinsicMatrix[0:-1, 0:-1], np.array([[dx], [dy], [dz]]))
        dx, dy, dz = vt[0][0], vt[1][0], vt[2][0]
        self.extrinsicMatrix = np.dot(self.newTranslationMatrix(dx, dy, dz), self.extrinsicMatrix)

    def rotate(self, axis, angle):
        self.extrinsicMatrix = np.dot(self.newRotationMatrix(axis, angle), self.extrinsicMatrix)

    def rotateOwnCenter(self, axis, angle):
        xc = np.mean(self.getPoints3d()[0, :])
        yc = np.mean(self.getPoints3d()[1, :])
        zc = np.mean(self.getPoints3d()[2, :])
        m = np.dot(self.newRotationMatrix(axis, angle), self.newTranslationMatrix(-xc, -yc, -zc))
        m = np.dot(self.newTranslationMatrix(xc, yc, zc), m)
        self.extrinsicMatrix = np.dot(m, self.extrinsicMatrix)

    def rotateOwnAxis(self, axis, angle):
        xc = np.mean(self.getWorldPoints()[0, :])
        yc = np.mean(self.getWorldPoints()[1, :])
        zc = np.mean(self.getWorldPoints()[2, :])
        m = np.dot(self.newRotationMatrix(axis, angle), self.newTranslationMatrix(-xc, -yc, -zc))
        m = np.dot(self.newTranslationMatrix(xc, yc, zc), m)
        self.extrinsicMatrix = np.dot(self.extrinsicMatrix, m)

    def getWorldPoints(self):
        return self.points

    def setWorldPoints(self, pts):
        self.points = pts

    def getBaseMatrix(self):
        return self.extrinsicMatrix[0:-1, 0:-1].T

    def getExtrinsicMatrix(self):
        return self.extrinsicMatrix

    def getPoints3d(self):
        return np.dot(self.getExtrinsicMatrix(), self.getWorldPoints())

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

    @staticmethod
    def draw_arrows(point, base, axis, length=1.5):
        for i in range(len(axis)):
            axis[i].quiver(point[0], point[1], point[2], base[0][0], base[0][1], base[0][2],
                           color='red', pivot='tail', length=length)
            axis[i].quiver(point[0], point[1], point[2], base[1][0], base[1][1], base[1][2],
                           color='green', pivot='tail', length=length)
            axis[i].quiver(point[0], point[1], point[2], base[2][0], base[2][1], base[2][2],
                           color='blue', pivot='tail', length=length)

    @staticmethod
    # Complementary functions for ploting points and vectors with Y-axis swapped with Z-axis
    def set_plots(ax=None, figure=None, figsize=(9, 8), limx=[-2, 2], limy=[-2, 2], limz=[-2, 2], naxis=1):
        if figure is None:
            figure = plt.figure(figsize=(9, 8))
        if ax is None:
            ax = []
            new_axis = True
        else:
            new_axis = False
        for i in range(naxis):
            if new_axis and naxis > 1:
                ax.append(figure.add_subplot(1, 2, i+1, projection='3d'))
            else:
                # ax = plt.axes(projection='3d')
                ax.append(figure.add_subplot(1, 1, 1, projection='3d'))

            ax[i].set_title("Camera Calibration")
            ax[i].set_xlim(limx)
            ax[i].set_xlabel("x axis")
            ax[i].set_ylim(limy)
            ax[i].set_ylabel("z axis")
            ax[i].set_zlim(limz)
            ax[i].set_zlabel("y axis")
        return ax
