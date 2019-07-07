# -*- coding: utf-8 -*-

""" Aluno: Leonardo Santos Paulucio
    Data: 06/05/19
    Trabalho 1 de Visão Computacional"""

import argparse
import textwrap

# My libraries
from Object import Object
from Camera import Camera
from Window import Window

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


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="python trab1.py",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent('''\
    Trabalho 1 de Visão Computacional - Transformações 3D e Projeção de Câmera

    Ex: Normal file: python trab1.py -f box.xyz (Default)
    Ex: STL file:    python trab1.py --stl -f models/mario.STL
    '''))

    parser.add_argument('--stl', '-s', action="store_true", dest="stl", default=False, required=False,
                        help='Use this flag if object file is stl')
    parser.add_argument('--file', '-f', default='box.xyz', dest='file',
                        help='Object file location')

    args = parser.parse_args()

    obj = Object()

    if args.stl:
        obj.loadSTL(args.file)
    else:
        obj.loadFile(args.file)
    cam = Camera()
    w = Window(cam, obj)
    w.show()
