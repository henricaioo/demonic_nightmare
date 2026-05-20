import pygame
from pygame import *
from sys import exit

import random as Rand
import os, sys
import getopt


pygame.init()

w = 1280
h = 720

perda = False
energia = True
som = True
office = True

mapadino = {
    'palco': ['lounge', 'manutencao'],
    'lounge': [ 'arcade' ],
    'manutencao': ['lounge'],
    'arcade':['portaa'],
    'portaa': ['escritorio'],
    'escritorio': []
}

mapagata = {
    'manutencao': ['lounge'],
    'lounge': ['som', 'cozinha'],
    'som':['lounge'],
    'cozinha': ['portab'],
    'portab': ['escritorio'],
    'escritorio': []
}

mapajoker = {
    'lounge': ['cozinha', 'arcade'],
    'cozinha': ['portab'],
    'arcade':['portaa'],
    'portaa': ['escritorio'],
    'portab': ['escritorio'],
    'escritorio': []
}

mapakangoo = {
    'palco': ['lounge', 'manutencao'],
    'manutencao': ['lounge'],
    'lounge': ['cozinha', 'arcade'],
    'cozinha': ['portab'],
    'arcade':['portaa'],
    'portaa': ['escritorio'],
    'portab': ['escritorio'],
    'escritorio': []
}

mapabat = {
    'palco': ['lounge', 'manutencao'],
    'lounge': ['cozinha'],
    'manutencao': ['lounge'],
    'cozinha': ['armazem', 'portab'],
    'armazem': ['gerador', 'cozinha'],
    'gerador':[],
    'portab': ['escritorio'],
    'escritorio': []
}


tela = pygame.display.set_mode((w, h))
pygame.display.set_caption('Demonic nightmare')
dirfile = os.path.dirname(os.path.abspath(__file__))
pasta_raiz = os.path.dirname(dirfile)
images_dir = os.path.join( pasta_raiz, "images" )
# 1. Carrega a imagem original (1920x1080)
caminho_imagem = os.path.join(images_dir, "office.png")
imagem_original = pygame.image.load(caminho_imagem).convert()

# 2. Redimensiona para o tamanho da sua tela (1280x720)
# Você pode usar as variáveis 'w' e 'h' que já definiu no topo do script
imagem_fundo = pygame.transform.scale(imagem_original, (w, h))

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
        self.vezes = 1
        self.update(0, 0, 0)


    def update(self, tempo, portaa, portab):
        global perda
        # verifica se o delay do personagem já acabou e se o jogo não foi perdido
        if tempo >= self.delay and perda == 0:
            # verifica se o personagem está em alguma porta e se 5 seg se passaram
            if self.pos == 'gerador' and (tempo - self.moved) >= 5000:
                global energia
                energia = False
                self.vezes += 1
                self.pos = self.inicial

            if self.pos == 'som' and (tempo - self.moved) >= 5000:
                global som
                som = False
                self.vezes += 1
                self.pos = self.inicial

            if self.pos == 'lounge' and 'som' in self.mapa and (tempo - self.moved) >= 5000:
                itens = self.mapa['lounge']
                pesos = [1, (1 * self.vezes)]
                self.cont = tempo
                num = Rand.randrange(1, 20)
                # se o numero gerado for menor ou igual a dificuldade do personagem, ele se move
                if num <= self.dif:
                    decidido = Rand.choices(itens, pesos)                    
                    self.moved = tempo
                    self.pos = decidido[0]
                    print("pos: ", self.pos)
                    print(self.moved)

            if self.pos == 'cozinha' and 'gerador' in self.mapa and (tempo - self.moved) >= 5000:
                itens = self.mapa['cozinha']
                pesos = [1, (1 * self.vezes)]
                self.cont = tempo
                num = Rand.randrange(1, 20)
                # se o numero gerado for menor ou igual a dificuldade do personagem, ele se move
                if num <= self.dif:
                    decidido = Rand.choices(itens, pesos)                    
                    self.moved = tempo
                    self.pos = decidido[0]
                    print("pos: ", self.pos)
                    print(self.moved)

            if self.pos == 'portaa' and (tempo - self.moved) >= 5000 :
                # caso afirmativo, verifica se a porta está aberta, se sim, ataca
                if portaa == 0:
                    perda = True
                    print(self.pos)
                    print('perdeu')
                else:
                    self.pos = self.inicial
                    self.moved = tempo
                    print('reset')

            elif self.pos == 'portab':
                print("portab")
                if (tempo - self.moved) >= 5000:
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
                    self.moved = tempo
                    self.pos = Rand.choice(self.mapa[self.pos])
                    print("pos: ", self.pos)
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
dino = Animatronic(5, 0, 'palco', mapadino, 2000)
#portab = Porta()
cameras = {
    'manutencao': pygame.Rect(85+900, 0+300, 120, 50),
    'palco': pygame.Rect(135+900, 60+300, 50, 20),
    'som': pygame.Rect(25+900, 60+300, 50, 50),
    'lounge': pygame.Rect(85+900, 90+300, 150, 120),
    'arcade': pygame.Rect(0+900, 180+300, 75, 150),
    'cozinha': pygame.Rect(85+900, 220+300, 70, 50),
    'armazem': pygame.Rect(165+900, 220+300, 70, 50),
    'gerador': pygame.Rect(165+900, 280+300, 70, 50)
}
cam = 'palco'

portaa = 0
portab = 0
hover = False


while True:
    tela.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for nome_cam, retangulo in cameras.items():
                if retangulo.collidepoint(mouse_pos):
                    cam = nome_cam

    

    if office != True:
        for nome_cam, retangulo in cameras.items():
            # Desenha o botão: cor clara se selecionada, escura se não
            cor = (150, 200, 120) if cam == nome_cam else (60, 60, 60)
            pygame.draw.rect(tela, cor, retangulo)
            # Borda para destacar o botão
            pygame.draw.rect(tela, (255, 255, 255), retangulo, 2)

        # desenho base do mapa na tela
        pygame.draw.rect(tela, (200, 200, 200), (85+900, 280+300, 70, 50))

        pygame.draw.rect(tela, (200, 200, 200), (75+900, 295+300, 10, 20))
        pygame.draw.rect(tela, (200, 200, 200), (110+900, 270+300, 20, 10))
        
        
        if dino.pos == cam and energia == True:
            pygame.draw.rect(tela, (255, 255, 0), (600, 350, 20, 20))

        if morcego.pos == cam and energia == True:
            pygame.draw.rect(tela, (255, 0, 255), (630, 350, 20, 20))
    else:
        tela.blit(imagem_fundo, (0, 0))

        botaoa = pygame.Rect(20, 20, 50, 30)
        botaob = pygame.Rect(80, 20, 50, 30)
        
        pos = pygame.mouse.get_pos()
        btnstatea = False
        btnstateb = False

        if botaoa.collidepoint(pos):
            pygame.draw.rect(tela, (200, 140, 160), botaoa)
            if pygame.mouse.get_pressed()[0] == 1 and btnstatea == False:
                btnstatea = True
                pygame.draw.rect(tela, (100, 200, 120), botaoa)
                portaa = 1

        elif botaob.collidepoint(pos):
            pygame.draw.rect(tela, (200, 140, 160), botaob)
            if pygame.mouse.get_pressed()[0] == 1 and btnstateb == False:
                btnstateb = True
                pygame.draw.rect(tela, (100, 200, 120), botaob)
                portab = 1
            
        else:
            pygame.draw.rect(tela, (200, 100, 80), botaoa)
            pygame.draw.rect(tela, (200, 100, 80), botaob)
            portab = 0
            portaa = 0
    
    mouse_pos = pygame.mouse.get_pos()
    aba_monitor = pygame.Rect(0, 680, 1280, 40)
    if aba_monitor.collidepoint(mouse_pos) and hover == False:
        hover = True
        office = not office # Se era True (Escritório), vira False (Câmeras) e vice-versa
    else:
        hover = False

    pygame.draw.rect(tela, (100, 100, 100), aba_monitor)
    tempo = pygame.time.get_ticks()
    morcego.update(tempo, portaa, portab)
    dino.update(tempo, portaa, portab)

    


    pygame.display.update()
    clock.tick(60)

    
