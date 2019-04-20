import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin


def getBaseMatrix():

    return np.array([[1, 0, 0]
                     [0, 1, 0]
                     [0, 0, 1]])


def getProjectionMatrix():

    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0]])


def getRotationMatrix(axis, angle):

    if axis == 'x':
        return np.array([[1,0,0,0], [0, cos(angle), -sin(angle),0],[0,sin(angle), cos(angle),0],[0,0,0,1]])

    elif axis == 'y':
        return np.array([[cos(angle), 0, sin(angle),0],[0,1,0,0],[-sin(angle), 0, cos(angle),0],[0,0,0,1]])

    elif axis == 'z':
        return np.array([[cos(angle), -sin(angle),0,0],[sin(angle),cos(angle),0,0],[0,0,1,0],[0,0,0,1]])


def getTranslationMatrix(dx, dy, dz):

    return np.array([[1, 0, 0, dx],
                     [0, 1, 0, dy],
                     [0, 0, 1, dz],
                     [0, 0, 0, 1]])


def getScaleMatrix(sx, sy, sz):

    return np.array([[sx, 0, 0, 0],
                     [0, sy, 0, 0],
                     [0, 0, sz, 0],
                     [0, 0, 0, 1]])


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
