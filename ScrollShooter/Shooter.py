import pygame
import os
import sys
import time
import Scripts
import random

FRAMETIME = 1/60
ENTITY_BASE_DATA = {'fire':0, 'fspd':0.5, 'vx':0, 'vy':0.5, 'dimg':0, 'bul':({'x': 0, 'y': 0, 'vx': 0, 'vy': 0.5, 'bimg': 1, 'dmg': 1}), 'simg':0, 'x':320, 'y':480, 'type':'enemy', 'hp':3, 'score':50, 'static':1, 'lives':0, 'level':0, 'levels':[], 'shield': 120}
OBJECT_BASE_DATA = {'x': 0, 'y': 0, 'oimg': 0, 'kill': 0, 'show': 1, 'setretimg': 0, 'script': 'pass'}
BULLET_BASE_DATA = {'x': 6, 'y': 8, 'vx': 0, 'vy': -5, 'bimg': 1, 'dmg': 1, 'aitime': 0, 'aispd': 0}


class Upgrade(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__(upg)
        self.data = {a: entitys[name][a] for a in entitys[name]}  
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
            if self.rect.y < -100 or self.rect.y > 640 or self.rect.x > 480 or self.rect.x < -100:
                self.kill()
        if mode == 1:
            eval(self.data['func'])
            self.kill()
    

class Object(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        super().__init__(obj)
        self.data = {}
        self.setup(OBJECT_BASE_DATA)
        self.setup(kwargs)
        self.rect.x = self.data['x']
        self.rect.y = self.data['y']
        
    def setup(self, kwargs):
        for _ in kwargs:
            self.data[_] = kwargs[_]
            if _ == 'oimg':
                self.image = oimages[self.data['oimg']]
                self.data['size'] = self.image.get_rect().size
                self.rect = self.image.get_rect()
                
    def update(self):
        data = {a: self.data[a] for a in self.data}
        data = eval(self.data['script'])
        if data['kill']:
            self.kill()
        if data['setretimg']:
            self.image = data['image']
            data['setretimg'] = 0
        self.rect.x = data['x']
        self.rect.y = data['y']
        if data['show'] == 0:
            self.image = deftex
        else:
            if data['oimg'] != self.data['oimg'] or self.data['show'] == 0:
                self.image = oimages[data['oimg']]
        self.data = {a: data[a] for a in data}


def cut(image):
    colorkey = image.get_at((0, 0))
    image.set_colorkey(colorkey)
    return image


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, data, camx):
        self.data = {}
        self.setup(BULLET_BASE_DATA)
        self.setup(data[0])
        self.setup(data[1])        
        if self.data['type'] == 'enemy':
            super().__init__(bull, ebull)
        else:
            super().__init__(bull)
        self.data['x'] += x
        self.data['y'] += y
        self.rect.x = self.data['x'] - camx
        self.rect.y = self.data['y']
        
    def setup(self, kwargs):
        for _ in kwargs:
            self.data[_] = kwargs[_]
            if _ == 'bimg':
                self.image = imagess[self.data['bimg']]
                self.data['size'] = self.image.get_rect().size
                self.rect = self.image.get_rect()

    def update(self, camx=0): # move&collidle
        if self.rect.y < -100 or self.rect.y > 640 or self.rect.x > 480 or self.rect.x < -100:
            self.kill()
        if self.data['aitime'] and self.data['type'] == 'enemy':
            data = player.sprites()[0].data
            posx = data['x'] - self.data['x'] + data['size'][0] // 2
            posy = data['y'] - self.data['y'] + data['size'][1] // 2
            dis = (posx ** 2 + posy ** 2) ** 0.5
            if dis != 0:
                vx = posx / dis * self.data['aispd']
                vy = posy / dis * self.data['aispd']
            else:
                posx = 0
                posy = 0
            self.data['aitime'] -= 1
            self.data['vx'] = vx
            self.data['vy'] = vy
        self.data['x'] += self.data['vx']
        self.data['y'] += self.data['vy']
        self.rect.x = self.data['x'] - camx
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
            self.basedata = {a: self.data[a] for a in self.data}
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
            self.data['shield'] -= 1
            self.data['fire'] += self.data['fspd']
            if self.data['fire'] > 1:
                self.data['fire'] -= 1
                for dat in self.data['bul']:
                    data = dat
                    Bullet(x=self.data['x'], y=self.data['y'], data=data, camx=camx)
            if self.data['type'] == 'player':
                h = pygame.sprite.spritecollide(self, ebull, False)
                if h:
                    h[0].kill()
                    player.update(mode=3)
                h = pygame.sprite.spritecollide(self, upg, False)
                for a in h:
                    score += a.data['score']
                    a.update(mode=1)                
        elif mode == 2: # setup
            self.setup(kwargs)
        elif mode == 3: # death
            if self.data['type'] == 'player' and self.data['shield'] < 0:
                if self.data['lives'] > 0:
                    self.basedata['lives'] = self.data['lives'] - 1
                    Entity(self.basedata)
                    self.kill()
                else:
                    self.data['fspd'] = 0
                    self.image = deftex
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
            if self.rect.y < -100 or self.rect.y > 640 or self.rect.x > 480 or self.rect.x < -100:
                self.kill()
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
        life = player.sprites()[0].data['lives']
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
        #do tick
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
        win.update(mode=1, camx=camx)
        bull.update(camx=camx)
        enemy.update(mode=1, camx=camx)
        enemy.update(camx=camx, mode=4)
        upg.update(camx=camx)
        obj.update()
        #frame change
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
        Object(num=_, x=x, script="scoreobj(data, score)")
    sc = obj.sprites()
    for _ in range(5):
        Object(num=_, x=_ * 12, y=23, oimg=11, script="livesobj(data, player.sprites()[0].data['lives'])")


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
    
def scoreobj(data, score):
    s = '0'
    if score > 0:
        s = str(score)[::-1]
    if len(s) > data['num']:
        data['show'] = 1
        data['oimg'] = int(s[data['num']])
    else:
        data['show'] = 0
    return data

def livesobj(data, lives):
    if data['num'] < lives:
        data['show'] = 1
    else:
        data['show'] = 0
    return data
    

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
deftex = pygame.Surface((0, 0))
camx = 0
score = 0
bgx = 0
bgy = 0
images = []
imagess = []
oimages = []
bg = []
emap = []
bullet = open('Bullets.txt').readlines()
bullets = {}
for a in bullet:
    aa = a.strip('\n').split('>')
    bullets[aa[0]] = eval(aa[1])
entity = open('Entity.txt').readlines()
entitys = {}
for a in entity:
    aa = a.strip('\n').split('>')
    entitys[aa[0]] = eval(aa[1])
