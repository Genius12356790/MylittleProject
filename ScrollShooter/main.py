from Shooter import *
pygame.display.set_caption("Shoot 'em 'up Engine")
cfg = [a.strip('\n').split('>') for a in open('config.cfg').readlines()]
cfg = {a[0]: a[1] for a in cfg}
topscore = int(cfg['top'][:-4])
s = sum([(int(a) + 1 + n) for n, a in enumerate(str(topscore))] + [49]) % 100
ss = sum([(int(a) + 11 + n) ** 2 for n, a in enumerate(str(topscore))] + [59]) % 100
if int(cfg['top'][-4:-2]) != s or int(cfg['top'][-2:]) != ss:
    topscore = 0
load_bg({' ': '4', '!': '0', '$': '2', '%': '3'})
win.update(1)
load_images(['1', '2', '0', '3', '4', '5', '6', '7', '8', '9', '10'])
load_object(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16'])
load_level('2')
load_map('3')
Object(x=160, y=150, oimg=14, frame=0, score=topscore, setretimg=0, script="Scripts.start(data, keys, oimages[:9])")
Entity(entitys['-2'])
initgame()
play(spd=0.1)
while True:
    load_level('2')
    load_map('2')
    player.update(mode=2, kwargs=entitys['-1'])
    play(spd=0.5)
    load_level('2')
    load_map('3')
    player.update(mode=2, kwargs=entitys['-2'])
    score = getscore()
    if score > topscore:
        topscore = score
        s = sum([(int(a) + 1 + n) for n, a in enumerate(str(score))] + [49]) % 100
        ss = sum([(int(a) + 11 + n) ** 2 for n, a in enumerate(str(score))] + [59]) % 100
        cfg['top'] = str(score) + str(s) + str(ss)
    with open('config.cfg', 'w') as file:
        file.write('\n'.join([a + '>' + str(cfg[a]) for a in cfg]))
    Object(x=160, y=150, oimg=14, frame=0, setretimg=0, score=topscore, script="Scripts.start(data, keys, oimages[:9])")
    play(spd=0.1)
    addevent('resetscore')