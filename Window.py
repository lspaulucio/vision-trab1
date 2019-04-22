# Standard libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

# My libraries
from Object import Object
from Camera import Camera
from Transforms import Transforms


class Window:

    def __init__(self, object, camera):
        self.obj = object
        self.cam = camera

    def showCamera3d(self, newFig=False):

        fig = self.fig

        if newFig == False:
            fig = plt.figure()

        quiver_ax = []

        for i in range(2):
            quiver_ax.append(fig.add_subplot(1,2,i+1,projection='3d'))
            quiver_ax[i].set_title("reference arrows example")
            quiver_ax[i].set_xlim([-2,2])
            quiver_ax[i].set_xlabel("x axis")
            quiver_ax[i].set_ylim([-2,2])
            quiver_ax[i].set_ylabel("y axis")
            quiver_ax[i].set_zlim([-2,2])
            quiver_ax[i].set_zlabel("z axis")
            Transforms.set_axes_equal(quiver_ax[i])

        # base vector values
        e1 = np.array([1, 0, 0])  # X
        e2 = np.array([0, 1, 0])  # Y
        e3 = np.array([0, 0, 1])  # Z

        points = self.cam.getPoints3d()
        # adding quivers to the plot

        for i in range(len(quiver_ax)):
            quiver_ax[i].quiver(points[0],points[1],points[2],e1,0,0,color='red',pivot='tail',  length=1)
            quiver_ax[i].quiver(points[0],points[1],points[2],0,e2,0,color='green',pivot='tail',length=1)
            quiver_ax[i].quiver(points[0],points[1],points[2],0,0,e3,color='blue',pivot='tail', length=1)

        # set camera view options of a plot
        quiver_ax[1].view_init(elev=90,azim=0)
        quiver_ax[1].dist=7
        plt.show()

    def show3d(self, obj):

        # ax0 = fig.add_subplot(2, 1, 2, projection='3d')
        points = obj.getWorldPoints()
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

    def show(self):

        fig = plt.figure()

        fig3d = fig.add_subplot(2,1,1, projection='3d')
        fig3d.set_title('3D World')
        fig3d.set_xlabel('x-axis')
        fig3d.set_ylabel('y-axis')
        fig3d.set_zlabel('z-axis')
        fig3d.set_xlim([-2, 2])
        fig3d.set_ylim([-1, 1])
        fig3d.set_zlim([4, 8])
        fig3d.view_init(elev=25, azim=-65)

        figProjection = fig.add_subplot(2,1,2)
        figProjection.set_title("Camera View")
        figProjection.set_xlabel("x-axis")
        figProjection.set_ylabel("y-axis")

        points = self.obj.getPoints3d()
        fig3d.plot3D(points[0, :], points[1, :], points[2, :], 'k.')
        Transforms.set_axes_equal(fig3d)

        projection = np.dot(Transforms.newProjectionMatrix(), self.obj.getPoints3d())
        projection = np.dot(self.cam.getIntrinsicMatrix(), projection)

        figProjection.plot(projection[0], projection[1], 'k.')
        # plt.draw()
        # plt.pause(0.001)
        # anim = animation.FuncAnimation(self.fig, self.update, frames=25, interval=50, blit=True)
        plt.show()
        plt.ion()


    def update(self):

        # Creating the Animation object
        points = self.obj.getPoints3d()
        self.fig3d.clear()
        self.fig3d.plot3D(points[0,:], points[1, :], points[2, :], 'k.')
        Transforms.set_axes_equal(self.fig3d)

        projection = np.dot(Transforms.newProjectionMatrix(), self.obj.getPoints3d())
        projection = np.dot(self.cam.getIntrinsicMatrix(), projection)

        self.figProjection.plot(projection[0], projection[1], 'k.')
        # plt.draw()
        # plt.pause(0.001)
        plt.ioff()
        plt.show(block=False)
