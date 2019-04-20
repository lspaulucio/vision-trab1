from Object import Object
from Window import Window
from Camera import Camera
import matplotlib.pyplot as plt
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

obj = Object()
obj.loadFile('box.xyz')
f = plt.figure()

c = Camera()
obj.show2d(c)
# obj.show3d(f)
# c.show()
# w = Window(obj, obj)
