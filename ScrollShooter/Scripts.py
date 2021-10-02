def pow0(data):
    if data['level'] + 1 < len(data['levels']):
        data['level'] += 1
        data['bul'] = data['levels'][data['level']].copy()
        
def pow1up(data):
    data['lives'] += 1