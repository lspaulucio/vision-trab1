import numpy as np
import matplotlib.pyplot as plt

from Object import Object
from Camera import Camera
from Transforms import Transforms


class Window:

    def __init__(self, obj, camera):
        self.plt = plt.Figure()

    def show2d(self, m):

        # fig = plt.figure()
        # ax0 = fig.add_subplot(2, 1, 1)
        # print (self.points.shape, self.translationMatrix.shape, self.rotationMatrix.shape)
        v = np.dot(self.rotationMatrix, self.translationMatrix)
        v = np.dot(v, self.points)
        v = np.dot(Transforms.getProjectionMatrix(), v)
        v = np.dot(m.getIntrinsicMatrix(), v)
        plt.plot(v[0], v[1], 'g.')
        plt.show()

    def show3d(self):

        # ax0 = fig.add_subplot(2, 1, 2, projection='3d')
        ax0 = plt.figure()
        ax0 = plt.axes(projection='3d')
        ax0.set_title('3D points')
        ax0.set_xlabel('x-axis')
        ax0.set_ylabel('y-axis')
        ax0.set_zlabel('z-axis')
        ax0.set_xlim([-2, 2])
        ax0.set_ylim([-1, 1])
        ax0.set_zlim([4, 8])
        ax0.plot3D(self.points[0, :], self.points[1, :], self.points[2, :], 'k.')
        ax0.view_init(elev=25, azim=-65)
        set_axes_equal(ax0)
        plt.show()
