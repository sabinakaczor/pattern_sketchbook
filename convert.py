import pickle

filename = 'files/szalik.pkl'
F = open(filename, 'rb')

old = pickle.load(F)

new = {
    'aspect_ratio': old['aspect_ratio'],
    'canvas_arr': {},
    'rows': len(old['cells']),
    'cols': len(old['cells'][0])
}

i = 0
for row in old['cells']:
    for col in old['cells'][row]:
        new['canvas_arr'][i] = {
            'row': row,
            'column': col,
            'color': old['cells'][row][col]['color']
        }
        i += 1

F_out = open(filename, 'wb')
pickle.dump(new, F_out)

