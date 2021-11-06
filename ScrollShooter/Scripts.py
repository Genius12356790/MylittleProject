import pygame
        
def pow1up(data):
    data['lives'] += 1
    
def hpbar(data, pld):
    data['px'] = data['spr'].data['hp'] / data['hp'] * (data['xs'])
    image = pygame.Surface(data['size'])
    image.blit(data['imageb'], (0, 0))
    col = (int(50 + 200 * data['spr'].data['hp'] / data['hp']), 50, 50)
    pygame.draw.rect(image, col, (data['xb'], data['yb'], data['px'], data['ys']))
    data['image'] = image
    data['setretimg'] = 1
    if data['px'] <= 0 and data['time'] < 0:
        data['time'] = 600
        data['eval'].append('Object(show=0, time=0, script="Scripts.transform(data, ebull)")')
        data['eval'].append('Object(show=0, time=0, script="Scripts.transform(data, enemy)")')
    if data['time'] == 0:
        '''data['script'] = "addevent('reset')"'''
        data['eval'].append('Object(x=5, y=50, oimg=17, strb=10, timb=10, fin={}, thrb=10, bon=1000, f=0, lives=player.sprites()[0].data, imageb=oimages[17], script="Scripts.win(data, oimages[:10], oimages[19:29], getscore())")'.format(data['fin']))
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
        
    
stars = 0
time = 0