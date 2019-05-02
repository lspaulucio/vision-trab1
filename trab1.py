# Standard libraries
from math import pi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, art3d
from matplotlib.widgets import RadioButtons, Slider
import numpy as np
import sys

# My libraries
from Object import Object
from Camera import Camera
from Transforms import Transforms


'''Trabalho 1 - Entrega até 06/05/2019

No primeiro trabalho vocês deverão fazer um programa onde será possível:

- visualizar a posição e orientação tridimensional de uma câmera e de um objeto;

- alterar a posição e orientação da câmera (parâmetros extrínsecos) e do objeto através de translações e
rotações tridimensionais;

- visualizar a imagem do objeto gerada pela câmera;

- alterar os parâmetros intrínsecos da câmera (distância focal, fator de escala de cada eixo, ponto principal)

- toda vez que algo for alterado, a visualização 3D e a imagem gerada pela câmera deverão ser atualizadas.

O trabalho poderá ser feito em dupla e deverá ser entregue/apresentado até o dia 06/05/2019.

Vocês deverão enviar o trabalho para raquel@ele.ufes.br até a data prevista e agendar a apresentação.'''


def update():
    fig3d.cla()
    fig3d.set_title('3D World')
    fig3d.set_xlabel('x-axis')
    fig3d.set_ylabel('y-axis')
    fig3d.set_zlabel('z-axis')
    fig3d.set_xlim([-3, 3])
    fig3d.set_ylim([-3, 3])
    fig3d.set_zlim([0, 8])

    objPoints = obj.getPoints3d()

    a = [fig3d]

    p = []
    p.append(np.mean(obj.getPoints3d()[0, :]))
    p.append(np.mean(obj.getPoints3d()[1, :]))
    p.append(np.mean(obj.getPoints3d()[2, :]))

    # Plotting object arrows
    Transforms.draw_arrows(p, obj.getBaseMatrix(), a)
    fig3d.plot3D(objPoints[0, :], objPoints[1, :], objPoints[2, :], 'k.')
    Transforms.set_axes_equal(fig3d)

    p = []
    p.append(cam.getPoints3d()[0])
    p.append(cam.getPoints3d()[1])
    p.append(cam.getPoints3d()[2])

    # Plotting camera arrows
    camPoints = cam.getPoints3d()
    Transforms.draw_arrows(p, cam.getBaseMatrix(), a)
    fig3d.plot3D(camPoints[0, :], camPoints[1, :], camPoints[2, :], 'k.')

    # Projection
    figProjection.cla()
    figProjection.set_title("Camera View")
    figProjection.set_xlabel("x-axis")
    figProjection.set_ylabel("y-axis")
    figProjection.set_xlim([-2, 2])
    figProjection.set_ylim([-1, 1])
    figProjection.set_aspect('equal')

    obj2Cam = np.dot(np.linalg.inv(cam.getExtrinsicMatrix()), obj.getPoints3d())
    projection = np.dot(Transforms.newProjectionMatrix(), obj2Cam)
    projection = np.dot(cam.getIntrinsicMatrix(), projection)

    id = projection[2, :] > 0
    # print(idx.shape)
    projection = projection[:, id]
    Z = projection[2]
    projection /= Z

    figProjection.plot(projection[0], projection[1], 'k.')
    fig.canvas.draw()
    # plt.ion()
    # plt.show()
    # plt.pause(0.001)


fig = plt.figure(figsize=(10, 10))
fig3d = fig.add_subplot(2, 1, 1, projection='3d')
figProjection = fig.add_subplot(2, 1, 2)

obj = Object()
obj.loadFile('box.xyz')
# obj.setWorldPoints(np.array([[0], [0], [5], [1]]))
cam = Camera()

elementSelected = obj
axisSelected = 'z'
transformSelected = 1

# Creating widgets
# plt.axes = left, bottom, width, height - position
objectButton = RadioButtons(plt.axes([0.0, 0.9, 0.17, 0.1]), ('Camera', 'Object'), active=1)
axisButton = RadioButtons(plt.axes([0.0, 0.8, 0.17, 0.1]), ('x', 'y', 'z'), active=2)
transformButton = RadioButtons(plt.axes([0.0, 0.7, 0.17, 0.1]), ('Translate', 'Rotate', 'Rotate Own Axis'), active=0)
focalDistance = Slider(plt.axes([0.15, 0.01, 0.3, 0.02]), 'Focal Distance', 1.0, 50.0, valinit=1.0, valstep=1)
mpX = Slider(plt.axes([0.15, 0.05, 0.3, 0.02]), 'Ox', -3.0, 3.0, valinit=0.0, valstep=0.5)
mpY = Slider(plt.axes([0.15, 0.03, 0.3, 0.02]), 'Oy', -3.0, 3.0, valinit=0.0, valstep=0.5)
scaleX = Slider(plt.axes([0.6, 0.05, 0.3, 0.02]), 'Sx', -10.0, 10.0, valinit=1.0, valstep=1)
scaleY = Slider(plt.axes([0.6, 0.03, 0.3, 0.02]), 'Sy', -10.0, 10.0, valinit=1.0, valstep=1)


def updateIntrinsicParameters(val):
    global cam
    f = focalDistance.val
    sx = scaleX.val
    sy = scaleY.val
    cam.setSx(sx)
    cam.setSy(sy)
    cam.setFocalDistance(f)
    cam.setOx(mpX.val)
    cam.setOy(mpY.val)
    update()


focalDistance.on_changed(updateIntrinsicParameters)
scaleX.on_changed(updateIntrinsicParameters)
scaleY.on_changed(updateIntrinsicParameters)
mpX.on_changed(updateIntrinsicParameters)
mpY.on_changed(updateIntrinsicParameters)


def objectSelection(label):
    objectDict = {'Camera': cam, 'Object': obj}
    global elementSelected
    elementSelected = objectDict[label]
    # print(elementSelected)


objectButton.on_clicked(objectSelection)


def axisSelection(label):
    global axisSelected
    axisSelected = label
    # print(axisSelected)


axisButton.on_clicked(axisSelection)


def transformSelection(label):
    transformDict = {'Translate': 1, 'Rotate': 2, 'Rotate Own Axis': 3}
    global transformSelected
    transformSelected = transformDict[label]
    # print(transformSelected)


transformButton.on_clicked(transformSelection)


def keyEventHandler(event):
    sys.stdout.flush()
    T_STEP = 0.5
    R_STEP = pi/6
    dx, dy, dz = 0, 0, 0
    if axisSelected == 'x':
        dx, dy, dz = T_STEP, 0, 0
    elif axisSelected == 'y':
        dx, dy, dz = 0, T_STEP, 0
    elif axisSelected == 'z':
        dx, dy, dz = 0, 0, T_STEP

    if event.key == 'up' or event.key == 'right':
        if transformSelected == 1:
            elementSelected.translate(dx, dy, dz)
        elif transformSelected == 2:
            elementSelected.rotate(axisSelected, R_STEP)
        elif transformSelected == 3:
            elementSelected.rotateSelf(axisSelected, R_STEP)

    elif event.key == 'down' or event.key == 'left':
        if transformSelected == 1:
            elementSelected.translate(-dx, -dy, -dz)
        elif transformSelected == 2:
            elementSelected.rotate(axisSelected, -R_STEP)
        elif transformSelected == 3:
            elementSelected.rotateSelf(axisSelected, -R_STEP)

    update()


update()
fig.canvas.mpl_connect('key_press_event', keyEventHandler)
plt.show()
