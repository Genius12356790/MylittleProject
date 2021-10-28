import pygame


def pow0(data):
    if data['level'] + 1 < len(data['levels']):
        data['level'] += 1
        data['bul'] = data['levels'][data['level']].copy()
        
def pow1up(data):
    data['lives'] += 1
    
def hpbar(data):
    data['px'] = data['spr'].data['hp'] / data['hp'] * (data['xs'])
    image = pygame.Surface(data['size'])
    image.blit(data['imageb'], (0, 0))
    col = (int(50 + 200 * data['spr'].data['hp'] / data['hp']), 50, 50)
    pygame.draw.rect(image, col, (data['xb'], data['yb'], data['px'], data['ys']))
    data['image'] = image
    data['setretimg'] = 1
    if data['px'] <= 0 and data['time'] < 0:
        data['time'] = 180
    if data['time'] == 1:
        data['script'] = "addevent('reset')"
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
    return data