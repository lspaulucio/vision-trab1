# -*- coding: utf-8 -*-

""" Aluno: Leonardo Santos Paulucio
    Data: 06/05/19
    Trabalho 1 de Visão Computacional"""

# Standard libraries
import sys
import numpy as np
from math import pi
from enum import Enum
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import art3d
from matplotlib.widgets import RadioButtons, Slider

# My libraries
from Camera import Camera
from Object import Object
from Transforms import Transforms


class tfType(Enum):
    TRANSLATE = 1
    ROTATE = 2
    ROTATE_OWN_CENTER = 3
    TRANSLATE_OWN_AXIS = 4


class Window():
    """ Class Window that show object and camera in the world"""

    def __init__(self, cam, obj):
        self.fig = plt.figure()
        self.fig3d = self.fig.add_subplot(2, 1, 1, projection='3d')
        self.figProjection = self.fig.add_subplot(2, 1, 2)
        self.obj = obj
        self.cam = cam
        self.elementSelected = self.obj
        self.axisSelected = 'z'
        self.transformSelected = tfType.TRANSLATE

    def update(self):
        self.fig3d.cla()
        self.fig3d.set_title('3D World')
        self.fig3d.set_xlabel('x-axis')
        self.fig3d.set_ylabel('y-axis')
        self.fig3d.set_zlabel('z-axis')
        self.fig3d.set_xlim([-3, 3])
        self.fig3d.set_ylim([-3, 3])
        self.fig3d.set_zlim([0, 8])

        objPoints = self.obj.getPoints3d()
        cam = self.cam
        obj = self.obj
        a = [self.fig3d]

        p = []
        p.append(np.mean(self.obj.getPoints3d()[0, :]))
        p.append(np.mean(self.obj.getPoints3d()[1, :]))
        p.append(np.mean(self.obj.getPoints3d()[2, :]))

        # Plotting object arrows
        Transforms.draw_arrows(p, obj.getBaseMatrix(), a)
        self.fig3d.plot3D(objPoints[0, :], objPoints[1, :], objPoints[2, :], 'k.')
        Transforms.set_axes_equal(self.fig3d)

        p = []
        p.append(cam.getPoints3d()[0])
        p.append(cam.getPoints3d()[1])
        p.append(cam.getPoints3d()[2])

        # Plotting camera arrows
        camPoints = cam.getPoints3d()
        Transforms.draw_arrows(p, cam.getBaseMatrix(), a)
        self.fig3d.plot3D(camPoints[0, :], camPoints[1, :], camPoints[2, :], 'k.')

        # Projection
        self.figProjection.cla()
        self.figProjection.set_title("Camera View")
        self.figProjection.set_xlabel("x-axis")
        self.figProjection.set_ylabel("y-axis")
        self.figProjection.set_xlim([-2, 2])
        self.figProjection.set_ylim([-1, 1])
        self.figProjection.set_aspect('equal')

        obj2Cam = np.dot(np.linalg.inv(cam.getExtrinsicMatrix()), obj.getPoints3d())
        projection = np.dot(Transforms.newProjectionMatrix(), obj2Cam)
        projection = np.dot(cam.getIntrinsicMatrix(), projection)

        indexes = projection[2, :] > 0
        # print(idx.shape)
        projection = projection[:, indexes]
        Z = projection[2]
        projection /= Z

        self.figProjection.plot(projection[0], projection[1], 'k.')
        self.fig.canvas.draw()
        # plt.ion()
        # plt.show()
        # plt.pause(0.001)

    def show(self):

        # Creating user interface

        # Creating widgets
        # plt.axes = left, bottom, width, height - box position
        objectButton = RadioButtons(plt.axes([0.0, 0.9, 0.17, 0.1]), ('Camera', 'Object'), active=1)
        axisButton = RadioButtons(plt.axes([0.0, 0.8, 0.17, 0.1]), ('x', 'y', 'z'), active=2)
        transformButton = RadioButtons(plt.axes([0.0, 0.7, 0.17, 0.1]), ('Translate', 'Rotate', 'Rotate Own Center', 'Translate Own Axis'), active=0)
        focalDistance = Slider(plt.axes([0.15, 0.01, 0.3, 0.02]), 'Focal Distance', 1.0, 50.0, valinit=1.0, valstep=0.5)
        mpX = Slider(plt.axes([0.15, 0.05, 0.3, 0.02]), 'Ox', -3.0, 3.0, valinit=0.0, valstep=0.5)
        mpY = Slider(plt.axes([0.15, 0.03, 0.3, 0.02]), 'Oy', -3.0, 3.0, valinit=0.0, valstep=0.5)
        scaleX = Slider(plt.axes([0.6, 0.05, 0.3, 0.02]), 'Sx', -10.0, 10.0, valinit=1.0, valstep=1)
        scaleY = Slider(plt.axes([0.6, 0.03, 0.3, 0.02]), 'Sy', -10.0, 10.0, valinit=1.0, valstep=1)

        def updateIntrinsicParameters(val):
            f = focalDistance.val
            sx = scaleX.val
            sy = scaleY.val
            self.cam.setSx(sx)
            self.cam.setSy(sy)
            self.cam.setFocalDistance(f)
            self.cam.setOx(mpX.val)
            self.cam.setOy(mpY.val)
            self.update()

        focalDistance.on_changed(updateIntrinsicParameters)
        scaleX.on_changed(updateIntrinsicParameters)
        scaleY.on_changed(updateIntrinsicParameters)
        mpX.on_changed(updateIntrinsicParameters)
        mpY.on_changed(updateIntrinsicParameters)

        def objectSelection(label):
            objectDict = {'Camera': self.cam, 'Object': self.obj}
            self.elementSelected = objectDict[label]

        objectButton.on_clicked(objectSelection)

        def axisSelection(label):
            self.axisSelected = label

        axisButton.on_clicked(axisSelection)

        def transformSelection(label):
            transformDict = {'Translate': tfType.TRANSLATE,
                             'Rotate': tfType.ROTATE,
                             'Rotate Own Center': tfType.ROTATE_OWN_CENTER,
                             'Translate Own Axis': tfType.TRANSLATE_OWN_AXIS}

            self.transformSelected = transformDict[label]

        transformButton.on_clicked(transformSelection)

        def keyEventHandler(event):
            """Function that waits for keyboard events"""

            sys.stdout.flush()
            T_STEP = 0.5
            R_STEP = pi/6
            dx, dy, dz = 0, 0, 0
            if self.axisSelected == 'x':
                dx, dy, dz = T_STEP, 0, 0
            elif self.axisSelected == 'y':
                dx, dy, dz = 0, T_STEP, 0
            elif self.axisSelected == 'z':
                dx, dy, dz = 0, 0, T_STEP

            if event.key == 'up' or event.key == 'right':
                if self.transformSelected == tfType.TRANSLATE:
                    self.elementSelected.translate(dx, dy, dz)
                elif self.transformSelected == tfType.ROTATE:
                    self.elementSelected.rotate(self.axisSelected, R_STEP)
                elif self.transformSelected == tfType.ROTATE_OWN_CENTER:
                    self.elementSelected.rotateOwnCenter(self.axisSelected, R_STEP)
                elif self.transformSelected == tfType.TRANSLATE_OWN_AXIS:
                    self.elementSelected.translateOwnAxis(dx, dy, dz)

            elif event.key == 'down' or event.key == 'left':
                if self.transformSelected == tfType.TRANSLATE:
                    self.elementSelected.translate(-dx, -dy, -dz)
                elif self.transformSelected == tfType.ROTATE:
                    self.elementSelected.rotate(self.axisSelected, -R_STEP)
                elif self.transformSelected == tfType.ROTATE_OWN_CENTER:
                    self.elementSelected.rotateOwnCenter(self.axisSelected, -R_STEP)
                elif self.transformSelected == tfType.TRANSLATE_OWN_AXIS:
                    self.elementSelected.translateOwnAxis(-dx, -dy, -dz)

            self.update()

        # End of interface

        self.update()
        self.fig.canvas.mpl_connect('key_press_event', keyEventHandler)
        plt.show()


if __name__ == "__main__":
    obj = Object()
    obj.loadFile('box.xyz')
    cam = Camera()

    w = Window(cam, obj)
    w.show()
