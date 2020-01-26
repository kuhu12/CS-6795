import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
with open('interactions_1554476728882_clean.json') as f:
	data = json.load(f)

players=[]
interactions=[]
unique_list = []
weight = []
elapsed_time_hover = []
elapsed_time_drag = []
first = []
second =[]
weight_list=[]

def pairwiseSum(lst, n): 
    sum = 0; 
    for i in range(len(lst)-1): 
        sum = lst[i] + lst[i + 1] 
        weight_list.append(sum)
     


for i in data:
	if (i['customLogInfo']['eventType']=='hover'):
		elapsed_time_hover.append(i['customLogInfo']['elapsedTime'])
	if(i['customLogInfo']['eventType']=='drag'):
		elapsed_time_drag.append(i['customLogInfo']['elapsedTime'])

max_elapsed_time_hover =  max(elapsed_time_hover)
min_elapsed_time_hover =  min(elapsed_time_hover)
max_elapsed_time_drag =  max(elapsed_time_drag)
min_elapsed_time_drag =  min(elapsed_time_drag)
new_max_drag = 1
new_min_drag = 2
new_max_hover = 0
new_min_hover = 1

for i in data:
	players.append(i['dataItem']['Name'])
	interactions.append(i['customLogInfo']['eventType'])

for i in data:
	if(i['customLogInfo']['eventType']=='click'):
		weight.append(3)
	if(i['customLogInfo']['eventType']=='hover'):
		x = i['customLogInfo']['elapsedTime'] 
		old_percent_hover = (x - min_elapsed_time_hover) / (max_elapsed_time_hover - min_elapsed_time_hover)
		new_x_hover = ((new_max_hover - new_min_hover) * old_percent_hover) + new_min_hover
		weight.append(new_x_hover)
	if(i['customLogInfo']['eventType']=='drag'):
		x = i['customLogInfo']['elapsedTime'] 
		old_percent_drag = (x - min_elapsed_time_drag) / (max_elapsed_time_drag - min_elapsed_time_drag)
		new_x_drag = ((new_max_drag - new_min_drag) * old_percent_drag) + new_min_drag
		weight.append(new_x_drag)

for i in range(len(players) - 1):
	first.append(players[i])
	second.append(players[i+1])

size = len(weight) 
pairwiseSum(weight, size) 

print(len(weight_list))

matrix_ad = pd.DataFrame({'source': first, "target": second, 'weight': weight_list})
per = matrix_ad.groupby(["source","target"]).size().reset_index(name="weight")
final= per.pivot_table(index='source',columns='target',values='weight')
final = final.fillna(0)

type_list = ['Player 47', 'Player 114', 'Player 127', 'Player 136', 'Player 166', 'Player 299', 'Player 310',
 'Player 324', 'Player 348', 'Player 383', 'Player 384', 'Player 394', 'Player 463', 'Player 473',
  'Player 597', 'Player 603', 'Player 611', 'Player 621', 'Player 852', 'Player 903', 'Player 51',
   'Player 79', 'Player 86', 'Player 134', 'Player 195', 'Player 213', 'Player 309', 'Player 433',
    'Player 496', 'Player 513', 'Player 571', 'Player 600', 'Player 702', 'Player 752', 'Player 771',
     'Player 799', 'Player 859', 'Player 920', 'Player 942', 'Player 966', 'Player 23', 'Player 107',
      'Player 113', 'Player 128', 'Player 161', 'Player 170', 'Player 335', 'Player 520', 'Player 562', 
      'Player 606', 'Player 678', 'Player 686', 'Player 762', 'Player 819', 'Player 824', 'Player 854',
       'Player 878', 'Player 959', 'Player 980', 'Player 995', 'Player 8', 'Player 11', 'Player 13', 'Player 30',
        'Player 49', 'Player 58', 'Player 162', 'Player 167', 'Player 253', 'Player 339', 'Player 391', 
        'Player 442', 'Player 554', 'Player 570', 'Player 763', 'Player 900', 'Player 919', 'Player 921',
		 'Player 952', 'Player 992', 'Player 85', 'Player 185', 'Player 199', 'Player 278', 'Player 289', 
		 'Player 380', 'Player 395', 'Player 537', 'Player 574', 'Player 585', 'Player 590', 'Player 640', 
		 'Player 689', 'Player 751', 'Player 755', 'Player 764', 'Player 828', 'Player 884', 'Player 887', 'Player 894']

#unique_list = list(set(players))
#unique_list = unique_list.sort()

plot_data = final.reindex(type_list, axis="columns")
plot_data_final = plot_data.reindex(type_list, axis="index")

plot_data_final.to_csv('type2_matrix_1554476728882.csv', encoding='utf-8')

plt.figure(figsize=(20,10))
ax = sns.heatmap(plot_data_final,cmap='Greens',xticklabels=True,yticklabels=True)
plt.savefig('type2_heatmap_1554476728882.png')