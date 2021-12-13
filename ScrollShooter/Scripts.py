import pygame
import random
import math
        
def pow1up(data):
    data['lives'] += 1
    
def hpbar(data, pld):
    data['px'] = data['spr'].data['hp'] / data['hp'] * (data['xs'])
    image = pygame.Surface(data['size'])
    image.blit(data['imageb'], (0, 0))
    col = (max(0, int(50 + 200 * data['spr'].data['hp'] / data['hp'])), 50, 50)
    pygame.draw.rect(image, col, (data['xb'], data['yb'], data['px'], data['ys']))
    data['image'] = image
    data['setretimg'] = 1
    if data['px'] <= 0 and data['time'] < 0:
        data['time'] = 600
        data['eval'].append('Object(show=0, time=0, script="Scripts.transform(data, ebull)")')
        data['eval'].append('Object(show=0, time=0, script="Scripts.transform(data, enemy)")')
    if data['time'] == 0:
        if data['win']:
            data['eval'].append('Object(x=5, y=50, oimg=17, strb=10, timb=10, fin={}, thrb=10, bon=1000, f=0, lives=player.sprites()[0].data, imageb=oimages[17], script="Scripts.win(data, oimages[:10], oimages[19:29], getscore())")'.format(data['fin']))
        else:
            data['eval'].append('addevent("reset")')
        data['eval'].append('Object(show=0, time=0, script="Scripts.kill(data, upg)")')
    return data

def start(data, keys, images):
    if data['frame'] == 0:
        data['setretimg'] = 1
        i = pygame.Surface((data['size'][0], data['size'][1] + 30))
        i.blit(data['image'], (0, 0))
        pt = data['size'][0] // 2 + 80
        for num in range(10):
            s = '0'
            if data['score'] > 0:
                s = str(data['score'])[::-1]
            if len(s) > num:
                i.blit(images[int(s[num])], (pt - num * 16, data['size'][1] + 14))
        data['image'] = i
    if keys[0]:
        data['time'] = 1
        data['script'] = "addevent('reset')"
    data['frame'] += 1
    if data['frame'] % 60 < 30:
        data['show'] = 0
    else:
        data['show'] = 1
    return data

def gameover(data, lives):
    if lives == -1:
        data['show'] = 1
        data['timetoret'] -= 1
        if data['timetoret'] == 0:
            data['time'] = 1
            data['script'] = "addevent('reset')"   
        stars = 0
    return data

def star(data, camx):
    global stars
    stars += 1
    data['eval'].append('Object(x={}, y={}, oimg=18, time=120)'.format(data['x'] - camx // 4, data['y'] - 12))
    return data
    
def timer(data):
    global time
    if data['sett'] == 0:
        time = data['t']
        data['sett'] = 1
    time -= 1
    return data

def kill(data, g):
    for i in g:
        i.kill()

def transform(data, g):
    for i in g:
        if (not 'hp' in i.data) or i.data['hp'] > 0:
            data['eval'].append('Upgrade(x={}, y={}, name="star")'.format(i.data['x'], i.data['y']))
    for i in g:
        i.kill()
    return data

def win(data, images, images2, score):
    global stars, time
    data['f'] += 1
    if data['f'] == 1:
        data['t'] = max(0, time // 60)
    if data['f'] >= 0:
        data['eval'].append('play_sound(2)')
        if data['t'] > 0:
            data['t'] -= 1
            data['timb'] += 1
            data['f'] = -5
            data['bon'] = data['strb'] * data['thrb'] * data['timb']
        elif stars > 0:
            data['f'] = -3
            stars -= 1
            data['strb'] += 1
            data['bon'] = data['strb'] * data['thrb'] * data['timb']
        elif data['bon'] > 100:
            data['bon'] -= 100
            data['f'] = -1
            data['eval'].append("setscore(score + 100)")
        elif data['bon'] > 0:
            data['eval'].append("setscore(score + data['bon'])")
            data['f'] = -90
            data['bon'] = 0
        elif data['lives']['lives'] > 0 and data['fin'] == 1:
            data['lives']['lives'] -= 1
            data['f'] = -90
            data['eval'].append("setscore(score + 10000)")
        else:
            data['eval'].append("addevent('reset')")
        i = pygame.Surface((data['size'][0], data['size'][1]))
        i.blit(data['imageb'], (0, 0))
        s = str(stars)[::-1]        
        for num in range(3):
            if len(s) > num:
                i.blit(images[int(s[num])], (440 - num * 16, 140))
        s = str(data['bon'])[::-1]        
        for num in range(10):
            if len(s) > num:
                i.blit(images2[int(s[num])], (430 - num * 25, 380))   
        s = str(data['t'])[::-1]        
        for num in range(3):
            if len(s) > num:
                i.blit(images[int(s[num])], (440 - num * 16, 65))          
        data['image'] = i      
        data['setretimg'] = 1
    return data


def shadow(data):
    if data['frame'] == 1:
        data['frame'] = 0
        np = [data['pd']['x'] - data['pd']['x'] // 4, data['pd']['y']]
        data['poses'].append(np)
        ln = len(data['poses'])
        if ln > 5:
            del data['poses'][0]
        if ln > data['num']:
            data['x'] = data['poses'][data['num']][0]
            data['y'] = data['poses'][data['num']][1]
            data['show'] = not [data['x'], data['y']] == np
    else:
        data['frame'] += 1
    return data


def b1_2_gun(data):
    offset = [_ // 2 for _ in data['target'].image.get_rect().size]
    data['angle'] = data['angle'] + data['rspd']
    data['target'].image = pygame.transform.rotate(data['bimage'],
                                         data['angle'])
    noffset = [_ // 2 for _ in data['target'].image.get_rect().size]
    pos = [data['target'].data['x'] + offset[0], data['target'].data['y'] + offset[1]]
    pos = [pos[_] - noffset[_] for _ in range(2)]
    data['target'].data['x'] = pos[0]
    data['target'].data['y'] = pos[1]
    data['target'].data['hitbox'] = [[0, 0, noffset[0] * 2, noffset[1] * 2, 1]]
    ang = data['angle'] - data['bangle']
    x = math.sin(ang * math.pi / 180)
    y = math.cos(ang * math.pi / 180)
    data['target'].data['bul'] = [[data['bul'], {'x':x * data['r'] + noffset[0] + data['xoff'], 'y':y * data['r'] + noffset[1] + data['yoff'], 'vx': x * data['spd'], 'vy': y * data['spd']}]]
    return data

def digittimer(data):
    global spd, y
    if y > 120000:
        y = 0
        spd = 0
        data['eval'].append('load_level("6")')
        data['eval'].append('win.update(mode=1)')
        data['eval'].append('addevent("spd=0")')
        data['eval'].append('Object(show=0, time=0, script="Scripts.transform(data, ebull)")')
        data['eval'].append('Object(show=0, time=0, script="Scripts.transform(data, enemy)")')      
    if spd or (data['l'] == 0):
        data['t'] -= 1.5
        data['setretimg'] = 1
        image = pygame.Surface((168, 32))
        if data['t'] > 0:
            divs = [36000, 3600, 600, 60, 10, 1]
            t = int(data['t'])
            pos = [0, 24, 60, 84, 120, 144]
            n = 0
            for i in divs:
                pn = t // divs[n]
                t = t % divs[n]
                image.blit(data['imageb'][pn], (pos[n], 0))
                n += 1   
        elif data['l'] == 1:
            spd = 0
            data['eval'].append('addevent("spd=0")')
            data['l'] = 0
            data['eval'].append('load_level("6")')
            data['eval'].append('win.update(mode=1)')
            data['eval'].append('Object(x=160, y=150, oimg=15)')
            data['eval'].append('Object(show=0, time=0, script="Scripts.kill(data, ebull)")')
            data['eval'].append('Object(show=0, time=0, script="Scripts.kill(data, enemy)")')  
            y = 0
            data['pd'].data['lives'] = 0
            data['pd'].update(mode=3)
        elif data['timetoret'] > 0:
            data['timetoret'] -= 1
        else:
            data['eval'].append('addevent("reset")')
        data['image'] = image
    else:
        data['timetoret'] -= 1
        if data['timetoret'] == 0:
            data['eval'].append('Object(x=5, y=50, oimg=17, strb=10, timb=10, fin=1, thrb=10, bon=1000, f=0, lives=player.sprites()[0].data, imageb=oimages[17], script="Scripts.win(data, oimages[:10], oimages[19:29], getscore())")')
            data['time'] = 0
    return data
        
def spdcontrol(data):
    global spd, y
    if data['spd']:
        spd = data['spd']
        data['spd'] = 0
    if spd != 0:
        spd += 1 / 3 ** (1 + int(spd * 10) / 100)
        data['eval'].append('addevent("spd={}")'.format(spd))
        y += spd
    else:
        data['time'] = 1
    return data

def spawner(data):
    data['t'] += data['rate']
    if spd == 0:
        data['time'] = 0    
    elif data['t'] > 1:
        data['t'] -= 1
        data['eval'].append(data['s'].format(random.randint(0, 600)))
        data['eval'].append(data['s2'].format(random.randint(0, 600)))
    return data

def metecon(data):
    global spd
    if data['target'].data['y'] > 640:
        data['time'] = 0
    hbbl = data['pd']['hitbox']
    posb = [data['pd']['x'], data['pd']['y']]
    hbal = data['target'].data['hitbox']
    posa = [data['target'].data['x'], data['target'].data['y']]
    flag = 0
    for hba in hbal:
        for hbb in hbbl:
            if (hba[0] + posa[0] <= hbb[2] + posb[0]) and (hba[2] + posa[0] >= hbb[0] + posb[0]) and (hba[1] + posa[1] <= hbb[3] + posb[1]) and (hba[3] + posa[1] >= hbb[1] + posb[1]) and hba[4] and hbb[4]:
                flag = 1
    if flag:
        spd = spd ** 0.5
        data['time'] = 0
        data['target'].kill()
    return data
        
stars = 0
time = 0
spd = 0
y = 0