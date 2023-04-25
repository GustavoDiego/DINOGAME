import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange

pasta_principal = os.path.dirname(__file__)
pasta_img = os.path.join(pasta_principal,'IMAGENS')
pasta_sons = os.path.join(pasta_principal,'SONS')


pygame.init()
pygame.mixer.init()



preto = (0,0,0)
branco = (255,255,255)
verde =(0,255,0)
vermelho = (255,0,0)
azul = (0,0,255)

largura = 640
altura = 480

tela = pygame.display.set_mode((largura,altura))
pygame.display.set_caption('DINO GAME')



sprite_sheet = pygame.image.load(os.path.join(pasta_img,'dinoSpritesheet.png')).convert_alpha()


som_morte = pygame.mixer.Sound(os.path.join(pasta_sons,'morte.wav'))
colidiu = False

class Dinossauro(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_dinossauro = []
        
        for i in range(3):     
                img = sprite_sheet.subsurface((i*32,0),(32,32))
                img = pygame.transform.scale(img,(32*3,32*3))
                self.imagens_dinossauro.append(img)
        
        self.som_pulo = pygame.mixer.Sound(os.path.join(pasta_sons,'pulo.wav'))
        self.index_lista = 0
        self.image =  self.imagens_dinossauro[self.index_lista]
        self.rect = self.image.get_rect()
        self.posy_inicial = altura-64 - 96//2
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (100,altura-64)
        self.pulo = False

    def pular(self):
        self.pulo = True
        self.som_pulo.play()
    def update(self):
         if self.pulo:
             if self.rect.y <= 200:
                 self.pulo = False
             self.rect.y -= 20
         else:
            if self.rect.y < self.posy_inicial:
                self.rect.y +=20
            else:
                self.rect.y = self.posy_inicial
         self.index_lista+= 0.25
         if self.index_lista > 2:
              self.index_lista = 0
         
         self.image = self.imagens_dinossauro[int(self.index_lista)]

  

todas_sprites = pygame.sprite.Group()
dino = Dinossauro()
todas_sprites.add(dino)


class Nuvem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = sprite_sheet.subsurface((7*32,0),(32,32))
        self.image = pygame.transform.scale(self.image,(32*3,32*3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50,200,50)
        self.rect.x = randrange(30,300,90)

        
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura
            self.rect.y = randrange(50,200,50)
        self.rect.x -= 10


for i in range(4):        
    nuvem = Nuvem()
    todas_sprites.add(nuvem)







class Chao(pygame.sprite.Sprite):
    
    def __init__(self, posx):
        pygame.sprite.Sprite.__init__(self)

        self.image = sprite_sheet.subsurface((6*32,0),(32,32))
        self.image = pygame.transform.scale(self.image,(32*2,32*2))
        self.rect = self.image.get_rect()
        self.rect.x = posx * 64
        self.rect.y = altura-64
    def update (self):
        if self.rect.topright[0]<0:
            self.rect.x = largura
        self.rect.x -= 10

for i in range(largura * 2 // 64):
    chao = Chao(i)
    todas_sprites.add(chao)
        

class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = sprite_sheet.subsurface((5*32,0),(32,32))
        self.image = pygame.transform.scale(self.image,(32*2,32*2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (largura,altura-64)
   
   
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura
        self.rect.x -= 10

cacto = Cacto()
todas_sprites.add(cacto)


grupo_obstaculos = pygame.sprite.Group()



grupo_obstaculos.add(cacto)


relogio = pygame.time.Clock()

while True:
    tela.fill(branco)
    relogio.tick(20)


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if dino.rect.y != dino.posy_inicial:
                    pass
                
                else:
                    dino.pular()
       
    colisoes = pygame.sprite.spritecollide(dino,grupo_obstaculos,False,pygame.sprite.collide_mask)
    
        
    todas_sprites.draw(tela)


    if colisoes and colidiu == False:
        som_morte.play()
        colidiu = True

    
    if colidiu == True:
        pass
    else:  
        todas_sprites.update()
        

    pygame.display.flip()

