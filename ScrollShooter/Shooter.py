import pygame
import os
import sys
import time
import Scripts
import random

FRAMETIME = 1/60
ENTITY_BASE_DATA = {'fire':0, 'simg':0, 'x':0, 'y':0, 'fspd':0, 'vx':0, 'vy':0, 'dimg':-1, 'bul':[], 'type':'enemy', 'spd':0, 'hp':0, 'score':0, 'static':1, 'lives':0, 'level':0, 'levels':[], 'shield': 120, 'large':0, 'times':[1], 'drop':[], 'hitbox':[]}
CUSTOM_BASE_DATA = {'simg':0, 'x':0, 'y':0, 'dimg':0, 'type':'enemy', 'lives': 0, 'hitbox': [], 'eval': [], 'vars': []}
OBJECT_BASE_DATA = {'x': 0, 'y': 0, 'oimg': 0, 'kill': 0, 'show': 1, 'setretimg': -1, 'script': 'pas(data)', 'time': -1}
BULLET_BASE_DATA = {'x': 6, 'y': 8, 'vx': 0, 'vy': -5, 'bimg': 1, 'dmg': 1, 'aitime': 0, 'aispd': 0, 'hitbox': []}
UPGRADE_BASE_DATA = {'vx':0, 'vy':0, 'simg':0, 'score':250, 'static':1, 'func':'pas(data)', 'sound':''}


class Upgrade(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__(upg)
        self.data = {}
        self.setup(UPGRADE_BASE_DATA)
        self.setup(entitys[name])
        #self.data = {a: entitys[name][a] for a in entitys[name]}  
        self.data['eval'] = []
        #self.image = imagess[self.data['simg']]
        self.rect = self.image.get_rect().move(x, y) 
        self.data['x'] = x
        self.data['y'] = y
    
    def setup(self, kwargs):
        for _ in kwargs:
            self.data[_] = kwargs[_]
            if _ == 'simg':
                self.image = imagess[self.data['simg']]
                self.data['size'] = self.image.get_rect().size
                self.rect = self.image.get_rect()
                
                
    def update(self, mode=0, camx=0):
        if mode == 0:
            self.data['x'] += self.data['vx']
            self.rect.x = self.data['x'] - camx
            self.data['y'] += self.data['vy']
            self.rect.y = self.data['y']
            if self.data['y'] < -100 or self.data['y'] > 640 or self.data['x'] > 640 or self.data['x'] < -100:
                self.kill()
        if mode == 1:
            data = eval(self.data['func'])
            if data:
                self.setup(data)
            for i in self.data['eval']:
                eval(i)
            if self.data['sound'] != '':
                play_sound(self.data['sound'])
            self.kill()
    

class Object(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        super().__init__(obj)
        self.data = {'eval': []}
        self.setup(OBJECT_BASE_DATA)
        self.setup(kwargs)
        self.rect.x = self.data['x']
        self.rect.y = self.data['y']
        if self.data['setretimg'] != -1:
            self.data['image'] = oimages[self.data['oimg']]
        if self.data['show'] == 0:
            self.image = deftex
        
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
        if data:
            for i in data['eval']:
                eval(i)
            data['eval'] = []
            if data['kill']:
                self.kill()
            if data['setretimg'] == 1:
                self.image = cut(data['image']).convert()
                self.data['size'] = data['image'].get_rect().size
                data['setretimg'] = 0
            self.rect.x = data['x']
            self.rect.y = data['y']
            if data['show'] == 0:
                self.image = deftex
            elif (data['oimg'] != self.data['oimg'] or self.data['show'] == 0) and data['setretimg'] == -1:
                    self.image = oimages[data['oimg']]
            elif self.data['show'] == 0 and data['setretimg'] == 0:
                self.image = data['image']
            self.data = {a: data[a] for a in data}
        if self.data['time'] == 0:
            self.kill()
        self.data['time'] -= 1        


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
        if self.data['hitbox'] == []:
            self.data['hitbox'].append([0, 0, self.data['size'][0], self.data['size'][1], 1])        
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
            h = enemy.sprites()
            for i in range(len(h)):
                for ii in h[i].data['hitbox']:
                    for iii in self.data['hitbox']:
                        if checkhb(ii[:4], [h[i].data['x'], h[i].data['y']], iii, [self.data['x'], self.data['y']]):
                            if ii[4]:
                                h[i].update(mode=3, dmg=self.data['dmg'])
                            self.kill()                        


class Entity(pygame.sprite.Sprite):
    def __init__(self, base, **kwargs):
        self.data = {}
        self.setup(ENTITY_BASE_DATA)
        self.setup(base)
        self.setup(kwargs)
        if self.data['hitbox'] == []:
            self.data['hitbox'] = [[0, 0, self.data['size'][0], self.data['size'][1], 1]]
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
            elif _ == 'shield':
                self.basedata = {a: self.data[a] for a in ['shield']}

    def update(self, mode=0, x=0, y=0, img=0, fspd=0.066, dmg=1, dimg=0, camx=0, kwargs={}, keys=[0, 0, 0, 0]):
        global score
        if mode == 0: # move player
            if keys[1]:
                self.data['x'] = max(self.data['x'] - self.data['spd'], 0)
            if keys[3]:
                self.data['x'] = min(self.data['x'] + self.data['spd'], 640 - self.data['size'][0])
            if keys[0]:
                self.data['y'] = max(self.data['y'] - self.data['spd'], 0)
            if keys[2]:
                self.data['y'] = min(self.data['y'] + self.data['spd'], 640 - self.data['size'][1])
            self.rect.x = self.data['x'] - camx
            self.rect.y = self.data['y']
        elif mode == 1: # tick
            self.data['shield'] -= 1
            for i in self.data['times']:
                if i >= self.data['fire'] and i <= self.data['fire'] + self.data['fspd']:
                    for dat in self.data['bul']:
                        data = dat
                        Bullet(x=self.data['x'], y=self.data['y'], data=data, camx=camx)
            self.data['fire'] = (self.data['fire'] + self.data['fspd']) % 1
            if self.data['type'] == 'player':
                h = ebull.sprites()
                for i in range(len(h)):
                    for ii in h[i].data['hitbox']:
                        for iii in self.data['hitbox']:
                            if checkhb(ii[:4], [h[i].data['x'], h[i].data['y']], iii, [self.data['x'], self.data['y']]):
                                if ii[4]:
                                    player.update(mode=3)
                                h[i].kill()               
                h = pygame.sprite.spritecollide(self, upg, False)
                for a in h:
                    score += a.data['score']
                    a.update(mode=1)                
        elif mode == 2: # setup
            self.setup(kwargs)
        elif mode == 3: # death
            if self.data['type'] == 'player' and self.data['shield'] < 0 and self.data['lives'] > -1:
                self.data['lives'] -= 1
                if self.data['lives'] >= 0:
                    self.data['level'] = 0
                    self.data['bul'] = self.data['levels'][0]
                    self.data['shield'] = self.basedata['shield']
                else:
                    self.data['fspd'] = 0
                    self.data['spd'] = 0
                    self.image = deftex
                    addevent('spd=0')
            elif self.data['type'] == 'enemy':
                self.data['hp'] -= dmg
                if self.data['hp'] < 1:
                    score += self.data['score']
                    for a in self.data['drop']:
                        if random.random() < a[1]:
                            Upgrade(self.data['x'] + self.data['size'][0] // 2 , self.data['y'] + self.data['size'][1] // 2, a[0])
                    self.data['drop'] = []
                    if self.data['dimg'] == -1:
                        self.kill()
                    else:
                        self.data['hitbox'] = []
                        self.data['fspd'] = 0
                        self.data['fire'] = 0.1122
                        self.image = imagess[self.data['dimg']]
        elif mode == 4: # set position
            self.data['x'] += self.data['vx']
            self.data['y'] += self.data['vy']
            self.rect.x = self.data['x'] - camx
            self.rect.y = self.data['y']
            if (self.rect.y < -100 or self.rect.y > 640 or self.rect.x > 480 or self.rect.x < -100)  and self.data['large'] == 0:
                self.kill()
        elif mode == 5: # entity with tiles
                self.data['y'] += y * self.data['static']
                
class CEntity(pygame.sprite.Sprite):
    def __init__(self, base, **kwargs):
        self.data = {}
        self.setup(CUSTOM_BASE_DATA)
        self.setup(base)
        self.setup(kwargs)
        if self.data['hitbox'] == []:
            self.data['hitbox'].append([0, 0, self.data['size'][0], self.data['size'][1], 1])        
        if self.data['type'] == 'player':
            super().__init__(player)
        else:
            super().__init__(enemy)
        self.u = self.data['script']
        
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
            elif _ == 'shield':
                self.basedata = {a: self.data[a] for a in ['shield']}
                
    def update(self, mode=0, x=0, y=0, img=0, fspd=0.066, dmg=1, dimg=0, camx=0, kwargs={}, keys=[0, 0, 0, 0]):
        global score
        self.u(self, mode=mode, x=x, y=y, img=img, fspd=fspd, dmg=dmg, dimg=dimg, camx=camx, kwargs=kwargs, keys=keys)
        for _ in self.data['eval']:
            eval(_)
        self.data['eval'] = []
    

class Tile(pygame.sprite.Sprite):
    def __init__(self, posa, posb):
        super().__init__(win)
        self.x = posa * 16
        self.y = posb * 16
        self.filex = posa
        self.filey = posb - 40        
        self.image = images[bg[self.filey % bgy][self.filex % bgx]]
        self.rect = self.image.get_rect().move(self.x, self.y) # width, height
        self.posa = posa
        self.posb = posb     

    def update(self, mode=0, camx=0, y=0):
        if mode == 0: # y-tick
            self.y += y
            if self.y >= 640:
                self.filey -= 39
                self.y -= 656
                self.image = images[bg[self.filey % bgy][self.filex % bgx]]
            self.rect.x = self.x - camx
            self.rect.y = self.y            
        if mode == 1: # reset
            self.x = self.posa * 16
            self.y = self.posb * 16
            self.filex = self.posa
            self.filey = self.posb - 40        
            self.image = images[bg[self.filey % bgy][self.filex % bgx]]
            self.rect = self.image.get_rect().move(self.x, self.y) # width, height  


def play(spd=0.5):
    global events, score
    camx = 0
    ypos = 0
    mappos = 0
    tick = 0
    lastframe = time.process_time()
    fps = 0
    fpsc = 0
    tps = 0
    tpsc = 0
    lastsec = 0
    while True:
        e = events
        events = []
        for i in e:
            if i == 'resetscore':
                score = 0
            elif i == 'reset':
                h = enemy.sprites()
                for i in range(len(h) - 1, -1, -1):
                    h[i].kill()
                h = bull.sprites()
                for i in range(len(h) - 1, -1, -1):
                    h[i].kill()     
                h = upg.sprites()
                for i in range(len(h) - 1, -1, -1):
                    h[i].kill()  
                h = obj.sprites()
                for i in range(len(h) - 1, 14, -1):
                    h[i].kill()  
                
                return
            elif i.split('=')[0] == 'spd':
                spd = float(i.split('=')[1])     
            elif i.split('=')[0] == 'score':
                score += int(i.split('=')[1])
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
        player.update(mode=1, camx=camx)
        player.update(keys=keys, camx=camx)
        tick += spd
        if tick > 1:
            y = tick // 1
            tick = tick % 1
            win.update(y=y, camx=camx)
            enemy.update(mode=5, y=y)
            ypos += y
            while len(emap) != mappos:
                if ypos >= int(emap[mappos].split('>')[0]):
                    eval(emap[mappos].split('>')[1])
                    mappos += 1
                else:
                    break
        else:
            win.update(camx=camx)
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
    textout('Engine ver. 0.9', [415, 625], size=10, color=(50, 50, 50))
    textout('enemy:' + str(len(enemy.sprites())), [435, 610], size=10, color=(50, 50, 50))
    textout('bull:' + str(len(bull.sprites())), [435, 595], size=10, color=(50, 50, 50))
    textout('obj:' + str(len(obj.sprites())), [435, 580], size=10, color=(50, 50, 50))
    textout('upg:' + str(len(upg.sprites())), [435, 565], size=10, color=(50, 50, 50))
    textout('ebull:' + str(len(ebull.sprites())), [435, 550], size=10, color=(50, 50, 50))
    textout('player:' + str(len(player.sprites())), [435, 535], size=10, color=(50, 50, 50))
    textout('win:' + str(len(win.sprites())), [435, 520], size=10, color=(50, 50, 50))
    pygame.display.flip()    
        
def initgame():
    for _ in range(40):
        for __ in range(41):
            Tile(_, __)
    for _ in range(10):
        x = (9 - _) * 16
        Object(num=_, x=x, script="scoreobj(data, score)")
    for _ in range(5):
        Object(num=_, x=_ * 12, y=23, oimg=11, script="livesobj(data, player.sprites()[0].data['lives'])")


def load_bg(spriteset):
    global images
    images = {a: pygame.image.load('BG/{}.png'.format(spriteset[a])).convert() for a in spriteset}


def load_images(spriteset):
    global imagess
    imagess = [cut(pygame.image.load('Pic/{}.png'.format(a))).convert_alpha() for a in spriteset]
    

def load_sounds(soundsset):
    global sounds
    sounds = [pygame.mixer.Sound('Sounds/' + a) for a in soundsset]


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
    oimages = [cut(pygame.image.load('Obj/{}.png'.format(a))).convert_alpha() for a in spriteset]
  
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

def pow0(data):
    if data['level'] + 1 < len(data['levels']):
        data['level'] += 1
        data['bul'] = data['levels'][data['level']].copy()

def pas(data):
    return data

def addevent(name):
    events.append(name)
    
def getscore():
    return score

def setscore(s):
    global score
    score = s
    
def play_sound(s):
    sounds[s].play()
    
def checkhb(hba, posa, hbb, posb):
    return (hba[0] + posa[0] <= hbb[2] + posb[0]) and (hba[2] + posa[0] >= hbb[0] + posb[0]) and (hba[1] + posa[1] <= hbb[3] + posb[1]) and (hba[3] + posa[1] >= hbb[1] + posb[1])

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
sounds = []
bg = []
emap = []
events = []
keys = [False] * 4
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