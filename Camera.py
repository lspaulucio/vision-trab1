import numpy as np
import matplotlib.pyplot as plt


class Camera:
    """ Object class"""

    def __init__(self):
        self.points = np.array([0, 0, 0, 1])
        self.f = 1
        self.sx = 1
        self.sy = 1
        self.so = 0
        self.ox = 0
        self.oy = 0

    def setFocalDistance(self, d):
        self.f = d

    def setOx(self, x):
        self.ox = x

    def setOy(self, y):
        self.oy = y

    # Arrumar ainda
    def getIntrinsicMatrix(self):
        return np.array([[self.f*self.sx, self.f*self.so, self.ox],
                         [0,              self.f*self.sy, self.oy],
                         [0,                     0,             1]])

    def show(self):
        fig_quivers = plt.figure(figsize=(10,5))
        quiver_ax = []
        for i in range(2):
            quiver_ax.append(fig_quivers.add_subplot(1,2,i+1,projection='3d'))
            quiver_ax[i].set_title("reference arrows example")
            quiver_ax[i].set_xlim([-2,2])
            quiver_ax[i].set_xlabel("x axis")
            quiver_ax[i].set_ylim([-2,2])
            quiver_ax[i].set_ylabel("y axis")
            quiver_ax[i].set_zlim([-2,2])
            quiver_ax[i].set_zlabel("z axis")

        # base vector values
        e1 = np.array([1, 0, 0])  # X
        e2 = np.array([0, 1, 0])  # Y
        e3 = np.array([0, 0, 1])  # Z

        # adding quivers to the plot
        for i in range(len(quiver_ax)):
            quiver_ax[i].quiver(self.points[0],self.points[1],self.points[2],e1,0,0,color='red',pivot='tail',  length=1)
            quiver_ax[i].quiver(self.points[0],self.points[1],self.points[2],0,e2,0,color='green',pivot='tail',length=1)
            quiver_ax[i].quiver(self.points[0],self.points[1],self.points[2],0,0,e3,color='blue',pivot='tail', length=1)

        # set camera view options of a plot
        quiver_ax[1].view_init(elev=90,azim=0)
        quiver_ax[1].dist=7

        plt.show()
