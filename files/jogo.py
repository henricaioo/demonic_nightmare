import pygame
from pygame import *
from sys import exit

import random as Rand
import os, sys
import getopt


pygame.init()

x = 0
y = 0

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


tela = pygame.display.set_mode((1280, 720))
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
        if tempo >= self.delay and perda == 0:
            if self.pos == 'portaa' and (tempo - self.moved) >= 3000 :
                if portaa == 0:
                    perda = 1
                    print(self.pos)
                    print('perdeu')
                else:
                    self.pos = self.inicial
                    self.moved = tempo
                    print('reset')

            elif self.pos == 'portab' and (tempo - self.moved) >= 3000:
                if portab == 0:
                    perda = 1
                    print(self.pos)
                    print('perdeu')
                else:
                    self.pos = self.inicial
                    self.moved = tempo
                    print('reset')

            elif (tempo - self.moved) >= 3000 and (tempo - self.cont) >= 2000:
                self.cont = tempo
                num = Rand.randrange(1, 20)
                if num <= self.dif:
                    self.pos = Rand.choice(self.mapa[self.pos])
                    print("pos: ", self.pos)
                    self.moved = tempo
                    print(self.moved)

        
              
        
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
portaa = Porta(235, 365, 10, 20)
portab = Porta(270, 340, 20, 10)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    tela.fill((0,0,0))
    pygame.draw.rect(tela, (100, 100, 100), (245, 70, 120, 50))
    pygame.draw.rect(tela, (100, 100, 100), (185, 130, 50, 50))
    pygame.draw.rect(tela, (100, 100, 100), (245, 130, 150, 150))
    pygame.draw.rect(tela, (100, 100, 100), (160, 250, 75, 150))
    pygame.draw.rect(tela, (100, 100, 100), (245, 290, 70, 50))
    pygame.draw.rect(tela, (100, 100, 100), (325, 290, 70, 50))
    pygame.draw.rect(tela, (100, 100, 100), (325, 350, 70, 50))
    pygame.draw.rect(tela, (200, 200, 200), (245, 350, 70, 50))
    

    tempo = pygame.time.get_ticks()
    portaa.doorcontrol()
    portab.doorcontrol()
    morcego.update(tempo, portaa.state, portab.state)
    


    pygame.display.update()
    clock.tick(60)

    
