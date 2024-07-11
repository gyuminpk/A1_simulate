from netpyne import specs
import pickle, json

netParams = specs.NetParams()   # object of class NetParams to store the network parameters

try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg import cfg

with open('cellDensity.pkl', 'rb') as fileObj: density = pickle.load(fileObj)['density']
density = {k: [x * cfg.scaleDensity for x in v] for k,v in density.items()} # Scale densities

density_re = {
    'L1' : {},
    'L2': {},
    'L3': {},
    'L4': {},
    'L5A': {},
    'L5B': {},
    'L6': {}

}

# ### LAYER 1:
density_re['L1']['NGF'] = density[('A1','nonVIP')][0]

### LAYER 2:

density_re['L2']['E'] = density[('A1','E')][1]
density_re['L2']['SOM'] = density[('A1','SOM')][1]
density_re['L2']['PV'] = density[('A1','PV')][1]
density_re['L2']['VIP'] = density[('A1','VIP')][1]
density_re['L2']['NGF'] = density[('A1','nonVIP')][1]


### LAYER 3:
density_re['L3']['E'] = density[('A1','E')][1]
density_re['L3']['SOM'] = density[('A1','SOM')][1]
density_re['L3']['PV'] = density[('A1','PV')][1]
density_re['L3']['VIP'] = density[('A1','VIP')][1]
density_re['L3']['NGF'] = density[('A1','nonVIP')][1]

### LAYER 4:

density_re['L4']['E'] = density[('A1','E')][2]
density_re['L4']['SOM'] = density[('A1','SOM')][2]
density_re['L4']['PV'] = density[('A1','PV')][2]
density_re['L4']['VIP'] = density[('A1','VIP')][2]
density_re['L4']['NGF'] = density[('A1','nonVIP')][2]

# # ### LAYER 5A:

density_re['L5A']['E'] = density[('A1','E')][3]
density_re['L5A']['SOM'] = density[('A1','SOM')][3]
density_re['L5A']['PV'] = density[('A1','PV')][3]
density_re['L5A']['VIP'] = density[('A1','VIP')][3]
density_re['L5A']['NGF'] = density[('A1','nonVIP')][3]


### LAYER 5B:
density_re['L5B']['E'] = density[('A1','E')][4]
density_re['L5B']['SOM'] = density[('A1','SOM')][4]
density_re['L5B']['PV'] = density[('A1','PV')][4]
density_re['L5B']['VIP'] = density[('A1','VIP')][4]
density_re['L5B']['NGF'] = density[('A1','nonVIP')][4]

# # ### LAYER 6:
density_re['L6']['E'] = density[('A1','E')][5]
density_re['L6']['SOM'] = density[('A1','SOM')][5]
density_re['L6']['PV'] = density[('A1','PV')][5]
density_re['L6']['VIP'] = density[('A1','VIP')][5]
density_re['L6']['NGF'] = density[('A1','nonVIP')][5]

total_array = []
per_array = []
layer_array=[]

for layer in density_re:
    layer_array.append(layer)
    total = 0
    temp = 0
    for cell in density_re[layer]:
        if cell == 'E':
            temp = density_re[layer][cell]
        total += density_re[layer][cell]

    density_re[layer]['total'] = total
    total_array.append(int(total))
    density_re[layer]['%'] = temp/total*100
    per_array.append(int(temp/total*100))

import matplotlib.pyplot as plt
import numpy as np


def draw_histogram(total_count, percentages):
    num_cells = len(percentages)
 # 모든 셀의 높이를 total_count로 설정

    fig, ax = plt.subplots()
    ax.bar(range(num_cells), total_count, color='lightblue')  # 전체 높이를 lightblue 색상으로 그림

    # 각 셀에 대해 %에 해당하는 부분을 다른 색으로 그리기
    for i, (cell, pct) in enumerate(zip(total_count, percentages)):
        ax.bar(i, cell * pct / 100, color='orange')  # 각 셀의 %에 해당하는 높이를 orange 색상으로 그림

    ax.set_xlabel('Cells')
    ax.set_ylabel('Counts')
    ax.set_title('Total neuron count and percentage of Exc Neuron')

    plt.xticks(range(num_cells), layer_array)  # 각 셀에 E1, E2, ... 레이블 설정
    plt.show()



draw_histogram(total_array, per_array)