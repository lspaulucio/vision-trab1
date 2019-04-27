# Standard libraries
from math import pi
# My libraries
from Object import Object
from Window import Window
from Camera import Camera


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

# GridSpec
# https://matplotlib.org/users/gridspec.html

if __name__ == "__main__":

    obj = Object()
    obj.loadFile('box.xyz')
    cam = Camera()
    w = Window(obj, cam)
    w.show()

    while (True):

        key = input("Choose an option:\nc - camera \
                                      \no - object \
                                      \ne - exit\n")

        # Object selected
        if key == 'o':
            key = input("Choose an option:\nt - Translate \
                                          \nro - Rotate Own Axis \
                                          \nr - Rotate\n")

            if key == 't':
                t = input("Enter with a translation vector: [dx, dy, dz]\n")
                t = t.replace('[', '')
                t = t.replace(']', '')
                t = [float(i) for i in t.split(',')]
                obj.translate(t[0], t[1], t[2])

            elif key == 'r':
                angle = float(input("Enter with an angle in degrees:\n"))
                angle *= pi/180
                axis = input("Enter with a axis [x, y or z]\n")
                obj.rotate(axis, angle)

            elif key == 'ro':
                angle = float(input("Enter with an angle in degrees:\n"))
                angle *= pi/180
                axis = input("Enter with a axis[x, y or z]\n")
                obj.rotateSelf(axis, angle)

        # Camera selected
        elif key == 'c':
            key = input("Choose a option:\nf - Focal distance \
                                         \nt - Translate \
                                         \nro - Rotate Own Axis \
                                         \nr - Rotate World\
                                         \ns - Scale Factor \
                                         \np - Main point\n")

            if key == 'f':
                f = input("Enter with a new focal distance f:\n")
                cam.setFocalDistance(float(f))

            elif key == 't':
                t = input("Enter with a translation vector: [dx, dy, dz]\n")
                t = t.replace('[', '')
                t = t.replace(']', '')
                t = [float(i) for i in t.split(',')]
                cam.translate(t[0], t[1], t[2])

            elif key == 'r':
                angle = float(input("Enter with an angle in degrees:\n"))
                angle *= pi/180
                axis = input("Enter with a axis[x, y or z]\n")
                cam.rotate(axis, angle)

            elif key == 'ro':
                angle = float(input("Enter with an angle in degrees:\n"))
                angle *= pi/180
                axis = input("Enter with a axis[x, y or z]\n")
                cam.rotateSelf(axis, angle)

            elif key == 's':
                t = input("Enter with the scale factor for x-axis and y-axis [sx, sy]:\n")
                t = t.replace('[', '')
                t = t.replace(']', '')
                t = [float(i) for i in t.split(',')]
                cam.setSx(t[0])
                cam.setSy(t[1])

            elif key == 'p':
                t = input("Enter with the new main position [ox, oy]:\n")
                t = t.replace('[', '')
                t = t.replace(']', '')
                t = [float(i) for i in t.split(',')]
                cam.setOx(t[0])
                cam.setOy(t[1])

        elif key == 'e':
            exit()

        w.show()
