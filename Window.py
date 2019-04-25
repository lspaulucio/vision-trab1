# Standard libraries
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, art3d

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

        # Plotting object in the world
        objPoints = self.obj.getPoints3d()
        fig3d = fig.add_subplot(2, 1, 1, projection='3d')
        fig3d.set_title('3D World')
        fig3d.set_xlabel('x-axis')
        fig3d.set_ylabel('y-axis')
        fig3d.set_zlabel('z-axis')
        fig3d.set_xlim([-3, 3])
        fig3d.set_ylim([-3, 3])
        fig3d.set_zlim([0, 10])


        # fig3d.view_init(elev=25, azim=-65)
        fig3d.plot3D(objPoints[0, :], objPoints[1, :], objPoints[2, :], 'k.')
        Transforms.set_axes_equal(fig3d)

        self.cam.points = np.array(self.obj.getWorldPoints())
        # self.cam.points = np.dot(Transforms.newScaleMatrix(0.5,1,1), self.cam.getWorldPoints())
        obj3d = np.dot(self.cam.getExtrinsicMatrix(), self.cam.getWorldPoints())

        # ax0 = self.set_plots()
        a = []
        a.append(fig3d)

        p = []
        p.append(np.mean(self.cam.getPoints3d()[0,:]))
        p.append(np.mean(self.cam.getPoints3d()[1,:]))
        p.append(np.mean(self.cam.getPoints3d()[2,:]))

        self.draw_arrows(p, self.cam.getBaseMatrix(), a)
        # OLHAR DIRECAO DO GIRO
        fig3d.plot3D(obj3d[0, :], obj3d[1, :], obj3d[2, :], 'c.')

        # Projection
        camPoints = self.cam.getWorldPoints()
        figProjection = fig.add_subplot(2, 1, 2)
        figProjection.set_title("Camera View")
        figProjection.set_xlabel("x-axis")
        figProjection.set_ylabel("y-axis")

        # ax0 = self.set_plots(figure=fig)
        # p = [0,0,0,1]
        # self.draw_arrows(p, Transforms.newBaseMatrix(), ax0)
        # t = np.linalg.inv(self.cam.getExtrinsicMatrix())
        # camPoints = np.dot(t, self.obj.getWorldPoints())
        projection = np.dot(Transforms.newProjectionMatrix(), objPoints)
        projection = np.dot(self.cam.getIntrinsicMatrix(), projection)

        # Z = projection[2]
        # projection /= Z

        # figProjection.plot(projection[0], projection[1], 'k.')
        # plt.draw()
        # plt.pause(0.001)
        # anim = animation.FuncAnimation(self.fig, self.update, frames=25, interval=50, blit=True)
        plt.show()
        plt.ion()
        # exit()

    @staticmethod
    def draw_arrows(point, base, axis, length=1.5):
        for i in range(len(axis)):
            axis[i].quiver(point[0],point[1],point[2],base[0][0],base[0][1],base[0][2],color='red',pivot='tail',  length=length)
            axis[i].quiver(point[0],point[1],point[2],base[1][0],base[1][1],base[1][2],color='green',pivot='tail',  length=length)
            axis[i].quiver(point[0],point[1],point[2],base[2][0],base[2][1],base[2][2],color='blue',pivot='tail',  length=length)
            # axis[i].quiver(point[0],point[2],point[1],base[0][0],base[0][2],base[0][1],color='red',pivot='tail',  length=length)
            # axis[i].quiver(point[0],point[2],point[1],base[2][0],base[2][2],base[2][1],color='blue',pivot='tail',  length=length)
            # axis[i].quiver(point[0],point[2],point[1],base[1][0],base[1][2],base[1][1],color='green',pivot='tail',  length=length)


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
                #ax = plt.axes(projection='3d')
                ax.append(figure.add_subplot(1, 1, 1, projection='3d'))

            ax[i].set_title("Camera Calibration")
            ax[i].set_xlim(limx)
            ax[i].set_xlabel("x axis")
            ax[i].set_ylim(limy)
            ax[i].set_ylabel("z axis")
            ax[i].set_zlim(limz)
            ax[i].set_zlabel("y axis")
        return ax
