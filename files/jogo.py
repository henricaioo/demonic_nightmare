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
# Carrega a imagem original (1920x1080)
caminho_office = os.path.join(images_dir, "office.png") # substitua pelo nome real do seu fundo padrão
img_office_aberto = pygame.image.load(caminho_office).convert()
img_office_aberto = pygame.transform.scale(img_office_aberto, (w, h))

# Escritório com Porta A fechada
caminho_portaa = os.path.join(images_dir, "office_portaa.png")
img_office_portaa = pygame.image.load(caminho_portaa).convert()
img_office_portaa = pygame.transform.scale(img_office_portaa, (w, h))

# Escritório com Porta B fechada
caminho_portab = os.path.join(images_dir, "office_portab.png")
img_office_portab = pygame.image.load(caminho_portab).convert()
img_office_portab = pygame.transform.scale(img_office_portab, (w, h))


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
                if num < self.dif:
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
                if num < self.dif:
                    self.moved = tempo
                    self.pos = Rand.choice(self.mapa[self.pos])
                    print("pos: ", self.pos)
                    print(self.moved)

class Dino(Animatronic):
    # Não precisamos reescrever o __init__ se ele for idêntico ao da classe mãe,
    # o Python já resolve isso automaticamente.

    def update(self, tempo, monitor_aberto, camera_atual):
        global perda
        
        if monitor_aberto and camera_atual == self.pos:
            return

        # Verifica se o delay inicial do personagem já acabou e se o jogo não foi perdido
        if tempo >= self.delay and perda == 0:
            
            # --- REGRA: Ignora a porta fechada ---
            # Se ele chegou na 'portaa' e passou dos 5 segundos, é Game Over direto,
            # sem checar se a 'portaa' está em 0 ou 1.
            if self.pos == 'portaa' and (tempo - self.moved) >= 5000:
                perda = True
                print(f"O {type(self).__name__} te pegou!")
                print('perdeu')
                return

            # --- Movimentação Padrão de Avanço ---
            # Caso não esteja na porta, dá o intervalo de 5 segundos para tentar se mover
            elif (tempo - self.moved) >= 5000 and (tempo - self.cont) >= 5000:
                self.cont = tempo
                num = Rand.randrange(1, 20)
                
                # Se o número gerado for menor ou igual à dificuldade, ele avança
                if num < self.dif:
                    self.moved = tempo
                    # Como seu 'mapadino' já é linear e não volta para trás,
                    # o Rand.choice vai apenas fazê-lo seguir em frente
                    self.pos = Rand.choice(self.mapa[self.pos])
                    print("Dino pos: ", self.pos)
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
dino = Dino(5, 0, 'palco', mapadino, 2000)
gata = Animatronic(5, 0, 'manutencao', mapagata, 5000)
joker = Animatronic(5, 0, 'lounge', mapajoker, 5000)
kangoo = Animatronic(5, 0, 'palco', mapakangoo, 5000)

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

# Controles do sistema de som
cooldown_som = 0       # Guarda o milissegundo em que o som estará liberado
vezes_som_usado = 0    # Multiplicador para aumentar o tempo de recarga
reparando_som = False  # Controla se o jogador está consertando o som
tempo_inicio_reparo = 0 # Guarda quando o reparo começou

while True:
    tela.fill((0,0,0))
    aba_monitor = pygame.Rect(0, 680, 1280, 40)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        # Gerencia cliques nas câmeras
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = event.pos
                
            if office != True: # Só clica nas câmeras se o monitor estiver aberto
                for nome_cam, retangulo in cameras.items():
                    if retangulo.collidepoint(mouse_pos):
                        cam = nome_cam
                # Cria o retângulo do botão de som no escritório (ajuste a posição se quiser)
                botao_som_audio = pygame.Rect(540, 600, 200, 50)
                
                if botao_som_audio.collidepoint(mouse_pos):
                    # Só funciona se o som NÃO estiver sabotado E o tempo atual passou do cooldown
                    if som == True and tempo >= cooldown_som:
                        dino.pos = dino.inicial # Reseta o Dino para o palco
                        dino.moved = tempo
                        print("Dino resetado pelo som!")
                        
                        vezes_som_usado += 1
                        # Adiciona 3 segundos de recarga por cada vez que já foi usado
                        cooldown_som = tempo + (vezes_som_usado * 3000) 
                    elif som == False:
                        print("O som está quebrado! Conserte-o pelas câmeras.")
                    else:
                        print(f"Som em recarga! Aguarde {int((cooldown_som - tempo)/1000)}s")

        # Gerencia o movimento do mouse na aba do monitor (Sem piscar)
        if event.type == MOUSEMOTION:
            if aba_monitor.collidepoint(event.pos):
                if not hover: # Se acabou de entrar na área
                    office = not office
                    hover = True
            else:
                hover = False

    

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
        
        if energia == True:
            if dino.pos == cam:
                pygame.draw.rect(tela, (255, 255, 0), (600, 350, 20, 20))

            if morcego.pos == cam:
                pygame.draw.rect(tela, (255, 0, 255), (630, 350, 20, 20))

            if kangoo.pos == cam:
                pygame.draw.rect(tela, (239, 228, 176), (660, 350, 20, 20))

            if joker.pos == cam:
                pygame.draw.rect(tela, (220, 20, 20), (690, 350, 20, 20))

            if gata.pos == cam:
                pygame.draw.rect(tela, (20, 220, 20), (720, 350, 20, 20))
                
            botao_som_audio = pygame.Rect(540, 600, 200, 50)   
            if som == False:
                cor_som = (255, 0, 0) # Vermelho se estiver sabotado
            elif tempo < cooldown_som:
                cor_som = (100, 100, 100)
            else:
                cor_som = (0, 150, 255) # Azul se estiver pronto para uso

            pygame.draw.rect(tela, cor_som, botao_som_audio)
            pygame.draw.rect(tela, (255, 255, 255), botao_som_audio, 2)

    else:
        if portaa == 0 and portab == 0:
            tela.blit(img_office_aberto, (0, 0))
            
        elif portab == 1:
            tela.blit(img_office_portab, (0, 0))
        elif portaa == 1:
            tela.blit(img_office_portaa, (0, 0))

        botao_som_audio = pygame.Rect(540, 600, 200, 50)
            

        # Define os retângulos dos botões
        botaoa = pygame.Rect(300, 200, 80, 50)
        botaob = pygame.Rect(850, 200, 80, 50)
        
        pos = pygame.mouse.get_pos()
        clicado = pygame.mouse.get_pressed()[0] == 1 # Guarda se o clique está pressionado

        # Reset padrão: Toda rodada do frame assume que estão abertas (soltou o mouse, elas abrem)
        portaa = 0
        portab = 0

        # Cores padrão dos botões (Abertas / Cor padrão)
        cor_a = (200, 100, 80)
        cor_b = (200, 100, 80)

        # Árvore de decisão de colisão e clique
        if botaoa.collidepoint(pos):
            if clicado:
                portaa = 1
                cor_a = (100, 200, 120) # Cor verde de ativa
            else:
                cor_a = (200, 140, 160) # Cor de hover (mouse em cima mas sem clicar)

        elif botaob.collidepoint(pos): # O 'elif' aqui já impede que as duas fechem juntas!
            if clicado:
                portab = 1
                cor_b = (100, 200, 120) # Cor verde de ativa
            else:
                cor_b = (200, 140, 160) # Cor de hover

        # 5. Desenha os botões na tela com as cores decididas acima
        pygame.draw.rect(tela, cor_a, botaoa)
        pygame.draw.rect(tela, cor_b, botaob)
    
    

    pygame.draw.rect(tela, (100, 100, 100), aba_monitor)
    tempo = pygame.time.get_ticks()
    #morcego.update(tempo, portaa, portab)
    dino.update(tempo, not office, cam)
    #gata.update(tempo,portaa, portab)
    #kangoo.update(tempo,portaa, portab)
    #joker.update(tempo,portaa, portab)
    

    


    pygame.display.update()
    clock.tick(60)

    
