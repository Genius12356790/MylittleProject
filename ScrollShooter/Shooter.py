import pygame
import os
import sys
import time
import Scripts
import random

FRAMETIME = 1/60
ENTITY_BASE_DATA = {'fire':0, 'fspd':0.5, 'vx':0, 'vy':0.5, 'dimg':0, 'bul':({'x': 0, 'y': 0, 'vx': 0, 'vy': 5, 'bimg': 1, 'dmg': 1}), 'simg':0, 'x':300, 'y':0, 'type':'enemy', 'hp':3, 'score':50, 'static':1}


class Upgrade(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__(upg)
        self.data = entitys[name]
        self.image = imagess[self.data['simg']]
        self.rect = self.image.get_rect().move(x, y) 
        self.data['x'] = x
        self.data['y'] = y
        
    def update(self, mode=0, camx=0):
        if mode == 0:
            self.data['x'] += self.data['vx']
            self.rect.x = self.data['x'] - camx
            self.data['y'] += self.data['vy']
            self.rect.y = self.data['y']
        if mode == 1:
            eval(self.data['func'])
            self.kill()
    


class Object(pygame.sprite.Sprite):
    def __init__(self, _, x, y):
        super().__init__(obj)
        self.image = oimages[0]
        self.image = self.image
        self.rect = self.image.get_rect().move(x, y)


def cut(image):
    colorkey = image.get_at((0, 0))
    image.set_colorkey(colorkey)
    return image


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, data, camx):
        if data['type'] == 'enemy':
            super().__init__(bull, ebull)
        else:
            super().__init__(bull)
        self.data = {}
        self.setup(data)
        self.data['x'] += x
        self.data['y'] += y
        self.rect.x = self.data['x'] - camx
        self.rect.y = self.data['y']
        
    def setup(self, kwargs):
        for _ in kwargs:
            self.data[_] = kwargs[_]
            if _ == 'bimg':
                self.image = imagess[self.data['bimg']]
                self.image = self.image
                self.data['size'] = self.image.get_rect().size
                self.rect = self.image.get_rect()

    def update(self, camx=0): # move&collidle
        if self.rect.y < -100 or self.rect.y > 740 or self.rect.x > 740 or self.rect.x < -100:
            self.kill()
        self.data['x'] += self.data['vx']
        self.rect.x = self.data['x'] - camx
        self.data['y'] += self.data['vy']
        self.rect.y = self.data['y']
        if self.data['type'] == 'player':
            h = pygame.sprite.spritecollide(self, enemy, False)
            if h:
                h[0].update(mode=3, dmg=self.data['dmg'])
                self.kill()


class Entity(pygame.sprite.Sprite):
    def __init__(self, base, **kwargs):
        self.data = {}
        self.setup(ENTITY_BASE_DATA)
        self.setup(base)
        self.setup(kwargs)
        if self.data['type'] == 'player':
            super().__init__(player)
        else:
            super().__init__(enemy)
        
    def setup(self, kwargs):
        for _ in kwargs:
            self.data[_] = kwargs[_]
            if _ == 'simg':
                self.image = imagess[self.data['simg']]
                self.image = self.image
                self.data['size'] = self.image.get_rect().size
                self.rect = self.image.get_rect().move(0, 0)
            elif _ == 'x':
                self.rect.x = self.data['x']
            elif _ == 'y':
                self.rect.y = self.data['y']

    def update(self, mode=0, x=0, y=0, img=0, fspd=0.066, dmg=1, dimg=0, camx=0, kwargs={}, keys=[0, 0, 0, 0]):
        global score
        if mode == 0: # move player
            if keys[1]:
                self.data['x'] = max(self.data['x'] - 2, 0)
            if keys[3]:
                self.data['x'] = min(self.data['x'] + 2, 640 - self.data['size'][0])
            if keys[0]:
                self.data['y'] = max(self.data['y'] - 2, 0)
            if keys[2]:
                self.data['y'] = min(self.data['y'] + 2, 640 - self.data['size'][1])
            self.rect.x = self.data['x'] - camx
            self.rect.y = self.data['y']
        elif mode == 1: # tick
            self.data['fire'] += self.data['fspd']
            if self.data['fire'] > 1:
                self.data['fire'] -= 1
                for dat in self.data['bul']:
                    data = dat
                    data['type'] = self.data['type']
                    Bullet(x=self.data['x'], y=self.data['y'], data=data, camx=camx)
            if self.data['type'] == 'player':
                h = pygame.sprite.spritecollide(self, ebull, False)
                if h:
                    player.update(mode=3)
                h = pygame.sprite.spritecollide(self, upg, False)
                for a in h:
                    score += a.data['score']
                    a.update(mode=1)                
        elif mode == 2: # setup
            self.setup(kwargs)
        elif mode == 3: # death
            if self.data['type'] == 'player':
                self.image = imagess[self.data['dimg']]
                self.data['fspd'] = 0                
            elif self.data['type'] == 'enemy':
                self.data['hp'] -= dmg
                if self.data['hp'] < 1:
                    score += self.data['score']
                    for a in self.data['drop']:
                        if random.random() < a[1]:
                            Upgrade(self.data['x'] + self.data['size'][0] // 2 , self.data['y'] + self.data['size'][1] // 2, a[0])
                    self.kill()
        elif mode == 4: # set position
            self.data['x'] += self.data['vx']
            self.data['y'] += self.data['vy']
            self.rect.x = self.data['x'] - camx
            self.rect.y = self.data['y']
        elif mode == 5: # entity with tiles
            if self.data['static']:
                self.rect.y += 1

class Tile(pygame.sprite.Sprite):
    def __init__(self, posa, posb):
        super().__init__(win)
        self.image = deftex
        self.x = posa * 16
        self.y = posb * 16
        self.rect = self.image.get_rect().move(self.x, self.y) # width, height
        self.filex = posa
        self.filey = posb - 40

    def update(self, mode=0, camx=0):
        if mode == 0: # y-tick
            self.y += 1
            if self.y >= 640:
                self.filey -= 39
                self.y = -16
                self.image = images[bg[self.filey % bgy][self.filex % bgx]]
        if mode == 1: # set position
            self.rect.x = self.x - camx
            self.rect.y = self.y
            self.image = images[bg[self.filey % bgy][self.filex % bgx]]


def play(spd=0.1):
    camx = 0
    ypos = 0
    mappos = 0
    tick = 0
    keys = [False] * 4
    lastframe = time.process_time()
    fps = 0
    fpsc = 0
    tps = 0
    tpsc = 0
    lastsec = 0
    while True:
        camx = player.sprites()[0].data['x'] // 4
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    keys[0] = True
                if event.key == pygame.K_LEFT:
                    keys[1] = True
                if event.key == pygame.K_DOWN:
                    keys[2] = True
                if event.key == pygame.K_RIGHT:
                    keys[3] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    keys[0] = False
                if event.key == pygame.K_LEFT:
                    keys[1] = False
                if event.key == pygame.K_DOWN:
                    keys[2] = False
                if event.key == pygame.K_RIGHT:
                    keys[3] = False
        player.update(keys=keys, camx=camx)
        player.update(mode=1, camx=camx)
        tick += spd
        if tick > 1:
            tick -= 1
            win.update()
            enemy.update(mode=5)
            ypos += 1
            while len(emap) != mappos:
                if ypos == int(emap[mappos].split('>')[0]):
                    eval(emap[mappos].split('>')[1])
                    mappos += 1
                else:
                    break
        s = score
        for sp in range(10):
            if s or not sp:
                sc[sp].image = oimages[s % 10]
            else:
                sc[sp].image = oimages[10]
            s = s // 10
        win.update(mode=1, camx=camx)
        bull.update(camx=camx)
        enemy.update(mode=1, camx=camx)
        enemy.update(camx=camx, mode=4)
        upg.update(camx=camx)
        obj.update()
        while time.process_time() < lastframe + FRAMETIME:
            pass
        lastframe += FRAMETIME
        prtime = time.process_time()
        if lastframe + 0.1 < prtime:
            lastframe = prtime          
        if lastframe + FRAMETIME > prtime:
            draw(fps, tps)       
            fpsc += 1               
        tpsc += 1
        if lastsec + 1 < prtime:
            lastsec = lastframe
            fps = fpsc
            fpsc = 0
            tps = tpsc
            tpsc = 0
            
def draw(fps, tps):
    #pygame.draw.rect(screen, (0, 0, 0), (0, 0, 480, 640))
    win.draw(screen)
    enemy.draw(screen)
    bull.draw(screen)
    player.draw(screen)
    upg.draw(screen)
    obj.draw(screen)  
    if fps < 0.9 * 1 / FRAMETIME:
        textout(str(fps), [400, 0], size=10, color=(250 * (1 / FRAMETIME - fps) * FRAMETIME, 250 * fps * FRAMETIME, 50))
    if tps < 0.95 * 1 / FRAMETIME:
        textout(str(int(tps * FRAMETIME * 100)) + '%', [430, 0], size=10, color=(250 * (1 / FRAMETIME - tps) * FRAMETIME, 250 * tps * FRAMETIME, 50))
    pygame.display.flip()    
        
def initgame():
    global sc
    for _ in range(40):
        for __ in range(41):
            Tile(_, __)
    for _ in range(10):
        x = (9 - _) * 16
        Object(_, x, 0)
    sc = obj.sprites()


def load_bg(spriteset):
    global images
    images = {a: pygame.image.load('BG/{}.png'.format(spriteset[a])).convert() for a in spriteset}


def load_images(spriteset):
    global imagess
    imagess = [cut(pygame.image.load('Pic/{}.png'.format(a))).convert() for a in spriteset]


def terminate():
    pygame.quit()
    sys.exit()


def load_level(num):
    global bgx, bgy, bg
    bg = [a.strip('\n') for a in open("BG/{}.txt".format(num), 'r').readlines()]
    bgy = len(bg)
    bgx = len(bg[0])


def load_map(num):
    global emap
    emap = [a.strip('\n') for a in open("BG/map{}.txt".format(num), 'r').readlines()]


def load_object(spriteset):
    global oimages
    oimages = [cut(pygame.image.load('Obj/{}.png'.format(a))).convert() for a in spriteset]
  
def textout(text, pos, size=30, font='Comic Sans MS', color=(255, 255, 255)):
    myfont = pygame.font.SysFont(font, size)
    textsurface = myfont.render(text, False, color)
    screen.blit(textsurface,(pos))

# init
pygame.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
size = width, height = 480, 640
screen = pygame.display.set_mode(size)
enemy = pygame.sprite.Group()
win = pygame.sprite.Group()
player = pygame.sprite.Group()
bull = pygame.sprite.Group()
ebull = pygame.sprite.Group()
obj = pygame.sprite.Group()
upg = pygame.sprite.Group()
deftex = pygame.Surface((1, 1))
camx = 0
score = 0
bgx = 0
bgy = 0
images = []
imagess = []
oimages = []
bg = []
emap = []
entity = open('Entity.txt').readlines()
entitys = {}
for a in entity:
    aa = a.strip('\n').split('>')
    entitys[aa[0]] = eval(aa[1])

