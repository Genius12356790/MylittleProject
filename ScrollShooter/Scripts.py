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
    if data['px'] <= 0:
        data['kill'] = 1
    return data