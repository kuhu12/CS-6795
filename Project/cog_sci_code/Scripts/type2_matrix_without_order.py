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

unique_list = list(set(players))
unique_list = unique_list.sort()


plot_data = pd.DataFrame(final, columns=unique_list)
plot_data.to_csv('type2_matrix_1554476728882.csv', encoding='utf-8')

plt.figure(figsize=(20,10))
ax = sns.heatmap(plot_data,cmap='Greens',xticklabels=True,yticklabels=True)
plt.savefig('type2_heatmap_1554476728882.png')