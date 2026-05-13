import pygame
from pygame import *
from sys import exit

import random as Rand
import os, sys
import getopt


pygame.init()

w = 1280
h = 720

perda = 0

mapadino = {
    'palco': ['lounge', 'manutencao'],
    'lounge': [ 'arcade' ],
    'manutencao': ['lounge'],
    'arcade':['portaa'],
    'portaa': ['escritorio']
}

mapagata = {
    'manutencao': ['lounge'],
    'lounge': ['som', 'cozinha'],
    'som':['lounge'],
    'cozinha': ['portab'],
    'portab': ['escritorio']
}

mapajoker = {
    'lounge': ['cozinha', 'arcade'],
    'cozinha': ['portab'],
    'arcade':['portaa'],
    'portaa': ['escritorio'],
    'portab': ['escritorio']
}

mapakangoo = {
    'palco': ['lounge', 'manutencao'],
    'manutencao': ['lounge'],
    'lounge': ['cozinha', 'arcade'],
    'cozinha': ['portab'],
    'arcade':['portaa'],
    'portaa': ['escritorio'],
    'portab': ['escritorio']
}

mapabat = {
    'palco': ['lounge', 'manutencao'],
    'lounge': ['cozinha'],
    'manutencao': ['lounge'],
    'cozinha': ['armazem', 'portab'],
    'armazem': ['gerador', 'cozinha'],
    'gerador':['armazem'],
    'portab': ['escritorio'],
    'escritorio': []
}


tela = pygame.display.set_mode((w, h))
pygame.display.set_caption('Demonic nightmare')
images_dir = os.path.join( "..", "imagens" )
clock = pygame.time.Clock()

class Animatronic(pygame.sprite.Sprite):
    def __init__(self, dif, stage, pos, mapa, delay, state = 0):
        pygame.sprite.Sprite.__init__( self )
        self.pos = pos
        self.dif = dif
        self.stage = stage
        self.moved = 0
        self.state = state
        self.cont = 0
        self.mapa = mapa
        self.inicial = pos
        self.delay = delay
        self.update(0, 0, 0)


    def update(self, tempo, portaa, portab):
        global perda
        # verifica se o delay do personagem já acabou e se o jogo não foi perdido
        if tempo >= self.delay and perda == 0:
            # verifica se o personagem está em alguma porta e se 5 seg se passaram
            if self.pos == 'portaa' and (tempo - self.moved) >= 5000 :
                # caso afirmativo, verifica se a porta está aberta, se sim, ataca
                if portaa == 0:
                    perda = 1
                    print(self.pos)
                    print('perdeu')
                else:
                    self.pos = self.inicial
                    self.moved = tempo
                    print('reset')

            elif self.pos == 'portab' and (tempo - self.moved) >= 5000:
                if portab == 0:
                    perda = 1
                    print(self.pos)
                    print('perdeu')
                else:
                    self.pos = self.inicial
                    self.moved = tempo
                    print('reset')

            # Caso não esteja na porta, dá um intervalo de 5 segundo e gera um número aleatorio
            elif (tempo - self.moved) >= 5000 and (tempo - self.cont) >= 5000:
                self.cont = tempo
                num = Rand.randrange(1, 20)
                # se o numero gerado for menor ou igual a dificuldade do personagem, ele se move
                if num <= self.dif:
                    self.pos = Rand.choice(self.mapa[self.pos])
                    print("pos: ", self.pos)
                    self.moved = tempo
                    print(self.moved)

class Cam(pygame.sprite.Sprite):
    def __init__(self, x, y, nome):
        self.x = x
        self.y = y
        self.nome = nome
              
        
class Porta(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, state = 0):
        self.state = state
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def doorcontrol(self):
        if self.state != 0:
            pygame.draw.rect(tela, (0, 255, 0), (self.x, self.y, self.w, self.h))
        else:
            pygame.draw.rect(tela, (255, 0, 0), (self.x, self.y, self.w, self.h))


morcego = Animatronic(5, 0, 'palco', mapabat, 2000)
dino = Animatronic(5, 0, 'palco', mapadino, 2000)
portaa = Porta(235, 365, 10, 20)
portab = Porta(270, 340, 20, 10)
cameras = {
    'manutencao': pygame.Rect(85, 0, 120, 50),
    'palco': pygame.Rect(135, 60, 50, 20),
    'som': pygame.Rect(25, 60, 50, 50),
    'lounge': pygame.Rect(85, 90, 150, 120),
    'arcade': pygame.Rect(0, 180, 75, 150),
    'cozinha': pygame.Rect(85, 220, 70, 50),
    'armazem': pygame.Rect(165, 220, 70, 50),
    'gerador': pygame.Rect(165, 280, 70, 50)
}
cam = 'palco'

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for nome_cam, retangulo in cameras.items():
                if retangulo.collidepoint(mouse_pos):
                    cam = nome_cam
                    print('muda de camera')

    tela.fill((0,0,0))

    for nome_cam, retangulo in cameras.items():
        # Desenha o botão: cor clara se selecionada, escura se não
        cor = (150, 200, 120) if cam == nome_cam else (60, 60, 60)
        pygame.draw.rect(tela, cor, retangulo)
        # Borda para destacar o botão
        pygame.draw.rect(tela, (255, 255, 255), retangulo, 2)

    # desenho base do mapa na tela
    pygame.draw.rect(tela, (200, 200, 200), (85, 280, 70, 50))
    

    tempo = pygame.time.get_ticks()
    portaa.doorcontrol()
    portab.doorcontrol()
    morcego.update(tempo, portaa.state, portab.state)

    if dino.pos == cam:
        pygame.draw.rect(tela, (255, 255, 0), (600, 350, 20, 20))

    if morcego.pos == cam:
        pygame.draw.rect(tela, (255, 0, 255), (630, 350, 20, 20))


    pygame.display.update()
    clock.tick(60)

    
