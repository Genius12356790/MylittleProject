import pygame
import os
import sys

FPS = 50


class Object(pygame.sprite.Sprite):
    def __init__(self, _, x, y):
        super().__init__(obj, sprites)
        self.image = oimages[0]
        self.image = cut(self.image)
        self.rect = self.image.get_rect().move(x, y)


def cut(image):
    colorkey = image.get_at((0, 0))
    image.set_colorkey(colorkey)
    return image


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, imn=0, bimn=0, bvx=0, bvy=0, vx=0, vy=0, static=0, fspd=0.02, hp=5, score=50):
        super().__init__(enemy, sprites)
        self.image = imagess[imn]
        self.image = cut(self.image)
        self.rect = self.image.get_rect().move(x, y)
        self.size = self.image.get_rect().size
        self.x = self.rect.x
        self.y = self.rect.y
        self.vx = vx
        self.vy = vy
        self.bvx = bvx
        self.bvy = bvy
        self.bimn = bimn
        self.static = static
        self.fire = 0
        self.fspd = fspd
        self.hp = hp
        self.score = score

    def update(self, mode=0, x=0, y=0, imn=0, ppos=0, vx=0, vy=0, dmg=1):
        global score
        if mode == 0:
            self.x += self.vx
            self.y += self.vy
            self.rect.x = int(self.x) + (ppos) // 5
            self.rect.y = int(self.y)
            self.fire += self.fspd
            if self.fire > 1:
                self.fire -= 1
                EBullet(self.rect.x, self.rect.y, self.size, imn=self.bimn, vx=self.bvx, vy=self.bvy, ppos=-ppos)
            if self.rect.y > 640 or self.rect.y < -100:
                self.kill()
        if mode == 1:
            self.hp -= 1
            if self.hp < 0:
                score += self.score
                self.kill()
        if mode == 2:
            self.y += 1 * 1 - self.static
            self.rect.y = y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, size=(16, 16), imn=0, vx=0, vy=0, ppos=0, dmg=1):
        super().__init__(bull, sprites)
        self.image = imagess[imn]
        self.image = cut(self.image)
        self.rect = self.image.get_rect()
        self.size = self.size = self.image.get_rect().size
        self.x = x + size[0] // 2 - self.size[0] // 2 + (ppos // 5)
        self.rect.x = self.x - ppos // 5
        self.rect.y = y + size[1] // 2 - self.size[1] // 2
        self.vx = vx
        self.vy = vy
        self.dmg = dmg

    def update(self, ppos=0):
        if self.rect.y < -100 or self.rect.y > 640 or self.rect.x > 600 or self.rect.x < -100:
            self.kill()
        self.x += self.vx
        self.rect.x = self.x + (ppos // 5)
        self.rect.y += self.vy
        h = pygame.sprite.spritecollide(self, enemy, False)
        if h:
            h[0].update(mode=1, dmg=self.dmg)
            self.kill()


class EBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, size=(16, 16), imn=0, vx=0, vy=0, ppos=0):
        super().__init__(ebull, sprites)
        self.image = imagess[imn]
        self.image = cut(self.image)
        self.rect = self.image.get_rect()
        self.size = self.size = self.image.get_rect().size
        self.x = x + size[0] // 2 - self.size[0] // 2 + (ppos // 5)
        self.rect.x = self.x - ppos // 5
        self.rect.y = y + size[1] // 2 - self.size[1] // 2
        self.vx = vx
        self.vy = vy

    def update(self, ppos=0):
        if self.rect.y < -100 or self.rect.y > 640:
            self.kill()
        self.x += self.vx
        self.rect.x = self.x + (ppos // 5)
        self.rect.y += self.vy


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player, sprites)
        self.image = imagess[0]
        self.image = cut(self.image)
        self.rect = self.image.get_rect().move(0, 0)
        self.size = self.image.get_rect().size
        self.fire = 0
        self.fspd = 0.066
        self.bimn = 0
        self.bvx = 0
        self.bvy = 0
        self.dmg = 1
        self.dimn = 0

    def update(self, mode=0, x=0, y=0, imn=0, fspd=0.066, dmg=1, dimn=0):
        if mode == 0:
            if x < 0:
                if self.rect.x + x >= 0:
                    self.rect.x += x
            if x > 0:
                if self.rect.x + x <= 480 - self.size[0]:
                    self.rect.x += x
            if y < 0:
                if self.rect.y + y >= 0:
                    self.rect.y += y
            if y > 0:
                if self.rect.y + y <= 640 - self.size[1]:
                    self.rect.y += y
        if mode == 1:
            self.fire += self.fspd
            if self.fire > 1:
                self.fire -= 1
                Bullet(self.rect.x, self.rect.y, self.size, imn=self.bimn, ppos=self.rect.x, vx=self.bvx, vy=self.bvy)
            h = pygame.sprite.spritecollide(self, ebull, False)
            if h:
                h[0].kill()
                self.image = cut(imagess[self.dimn])
                self.fspd = 0
        if mode == 2:
            self.fspd = fspd
            self.image = imagess[imn]
            self.image = cut(self.image)
            self.size = self.image.get_rect().size
            self.dmg = dmg
            self.dimn = dimn
        if mode == 3:
            self.bimn = imn
            self.bvx = x
            self.bvy = y
        if mode == 4:
            self.rect.x = x
            self.rect.y = y


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(win, sprites)
        pos += (pos // 31) * 8
        self.image = images[0]
        self.rect = self.image.get_rect().move(
            16 * (pos % 39), 16 * (pos // 39))  # width, height
        self.pos = pos
        self.basepos = pos
        self.poss = pos
        self.mx = 0

    def update(self, mode=0, x=0, y=0, ppos=0):
        if mode == 0:
            self.rect.y += 1
            if self.rect.y >= 640:
                self.poss -= 39
                self.rect.y = -16
                mx = ppos // 80
                self.mx = mx
                self.pos = self.poss - mx
                self.image = images[ord(bg[((self.pos // 39) - 41) % bgy][(self.pos % 39) % bgx]) - 32]
        if mode == 1:
            self.pos = self.basepos
            pos = self.pos
            self.rect.x = 16 * (pos % 39)
            self.rect.y = 16 * (pos // 39) - 16
            self.image = images[ord(bg[((self.pos // 39) - 41) % bgy][(self.pos % 39) % bgx]) - 32]
        if mode == 2:
            mx = ppos // 80
            if self.mx != mx:
                self.mx = mx
                self.pos = self.poss - mx
                self.image = images[ord(bg[((self.pos // 39) - 41) % bgy][(self.pos % 39) % bgx]) - 32]
            self.rect.x = (self.poss % 39) * 16 - 16 + (ppos // 5) % 16


def play(spd=0.1):
    ypos = 0
    mappos = 0
    tick = 0
    win.update(mode=1)
    keys = [False] * 4
    while True:
        ppos = -player.sprites()[0].rect.x
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
        if keys[0]:
            player.update(y=-2)
        if keys[1]:
            player.update(x=-2)
        if keys[2]:
            player.update(y=2)
        if keys[3]:
            player.update(x=2)
        player.update(mode=1)
        tick += spd
        if tick > 1:
            tick -= 1
            win.update()
            enemy.update(mode=2)
            ypos += 1
            while len(emap) != mappos:
                if ypos == int(emap[mappos].split(':')[0]):
                    eval(emap[mappos].split(':')[1])
                    mappos += 1
                else:
                    break
        s = score
        for sp in range(10):
            if s or not sp:
                sc[sp].image = cut(oimages[s % 10])
            else:
                sc[sp].image = cut(oimages[10])
            s = s // 10
        win.update(mode=2, ppos=ppos)
        bull.update(ppos=ppos)
        ebull.update(ppos=ppos)
        enemy.update(ppos=ppos)
        obj.update()
        win.draw(screen)
        enemy.draw(screen)
        bull.draw(screen)
        ebull.draw(screen)
        player.draw(screen)
        obj.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def load_bg(spriteset):
    return [pygame.image.load('BG/{}.png'.format(a)) for a in spriteset]


def load_images(spriteset):
    return [pygame.image.load('Pic/{}.png'.format(a)) for a in spriteset]


def terminate():
    pygame.quit()
    sys.exit()


def load_level(num):
    return [a.strip('\n') for a in open("BG/{}.txt".format(num), 'r').readlines()]


def load_map(num):
    return [a.strip('\n') for a in open("BG/map{}.txt".format(num), 'r').readlines()]


def load_object(spriteset):
    return [pygame.image.load('Obj/{}.png'.format(a)) for a in spriteset]


def toeq(var, data):
    return [var, data]


# init
pygame.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
size = width, height = 480, 640
screen = pygame.display.set_mode(size)
enemy = pygame.sprite.Group()
sprites = pygame.sprite.Group()
win = pygame.sprite.Group()
player = pygame.sprite.Group()
bull = pygame.sprite.Group()
ebull = pygame.sprite.Group()
obj = pygame.sprite.Group()
score = 0
images = load_bg(['0'])
imagess = load_images(['0'])
oimages = load_object(['0'])
clock = pygame.time.Clock()
for _ in range(31 * 41):
    Tile(_)
Player()
for _ in range(10):
    x = (9 - _) * 16
    Object(_, x, 0)
sc = obj.sprites()

# main
mainscript = open('main.txt')
for a in mainscript:
    data = eval(a)
    if data:
        if data[0] == 'bg':
            bg = data[1]
            bgy = len(bg)
            bgx = len(bg[0])
        if data[0] == 'images':
            images = data[1]
        if data[0] == 'imagess':
            imagess = data[1]
        if data[0] == 'emap':
            emap = data[1]
        if data[0] == 'obj':
            oimages = data[1]
terminate()
