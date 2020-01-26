import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
with open('interactions_1552418101507_clean.json') as f:
	data = json.load(f)

print(len(data))

prev_value = ''
for i in data[:]:
	if(i['dataItem']['Name'] == prev_value):
		data.remove(i)
	else:
		prev_value = i['dataItem']['Name']

print(len(data))


new_data=[]


for i in data:
	player_name = i['dataItem']['Name']
	data_loc = i['customLogInfo']['data_locations']
	quadrant = ''
	for q in data_loc:
		if q['player'] == player_name:
			if  (0 <= q['cx'] < 283.33) and (0 <= q['cy'] < 116.66):
				quadrant = 'A'
			elif (283.33 <= q['cx'] < 566.66) and (0 <= q['cy'] < 116.66):
				quadrant = 'B'
			elif (566.66 <= q['cx'] <= 850) and (0 <= q['cy'] < 116.66):
				quadrant = 'C'
			elif  (0 <= q['cx'] < 283.33) and (116.66 <= q['cy'] < 233.33):
				quadrant = 'D'
			elif (283.33 <= q['cx'] < 566.66) and (116.66 <= q['cy'] < 233.33):
				quadrant = 'E'
			elif (566.66 <= q['cx'] <= 850) and (116.66 <= q['cy'] < 233.33):
				quadrant = 'F'
			elif  (0 <= q['cx'] <= 283.33) and (233.33 <= q['cy'] <= 350):
				quadrant = 'G'
			elif (283.33 <= q['cx'] < 566.66) and (233.33 <= q['cy'] <= 350):
				quadrant = 'H'
			elif (566.66 <= q['cx'] <= 850) and (233.33 <= q['cy'] <= 350):
				quadrant = 'I'
	event_type = i['customLogInfo']['eventType']
	if(event_type == 'click'):
		duration = 0
	else:
		duration = i['customLogInfo']['elapsedTime'] 
	myjson_object = {
                'Quadrant': quadrant,
                'Event': event_type,
                'Duration': duration
            }
	new_data.append(myjson_object)


elapsed_time_hover = []
elapsed_time_drag = []
weight = []
weight_list=[]

def pairwiseSum(lst, n): 
    sum = 0; 
    for i in range(len(lst)-1): 
        sum = lst[i] + lst[i + 1] 
        weight_list.append(sum)

for i in new_data:
	if (i['Event'] == 'hover'):
		elapsed_time_hover.append(i['Duration'])
	if(i['Event']=='drag'):
		elapsed_time_drag.append(i['Duration'])

max_elapsed_time_hover =  max(elapsed_time_hover)
min_elapsed_time_hover =  min(elapsed_time_hover)
max_elapsed_time_drag =  max(elapsed_time_drag)
min_elapsed_time_drag =  min(elapsed_time_drag)
new_max_drag = 1
new_min_drag = 2
new_max_hover = 0
new_min_hover = 1

for i in new_data:
	if(i['Event']=='click'):
		weight.append(3)
	if(i['Event']=='hover'):
		x = i['Duration'] 
		old_percent_hover = (x - min_elapsed_time_hover) / (max_elapsed_time_hover - min_elapsed_time_hover)
		new_x_hover = ((new_max_hover - new_min_hover) * old_percent_hover) + new_min_hover
		weight.append(new_x_hover)
	if(i['Event']=='drag'):
		x = i['Duration']
		old_percent_drag = (x - min_elapsed_time_drag) / (max_elapsed_time_drag - min_elapsed_time_drag)
		new_x_drag = ((new_max_drag - new_min_drag) * old_percent_drag) + new_min_drag
		weight.append(new_x_drag)


quadrants=[]

for i in new_data:
	quadrants.append(i['Quadrant'])

first = []
second =[]
for i in range(len(quadrants) - 1):
	first.append(quadrants[i])
	second.append(quadrants[i+1])


size = len(weight) 
pairwiseSum(weight, size) 


matrix_ad = pd.DataFrame({'source': first, "target": second, 'weight': weight_list})
per = matrix_ad.groupby(["source","target"]).size().reset_index(name="weight")
final= per.pivot_table(index='source',columns='target',values='weight')



type_list = ['A', 'B', 'C','D','E','F','G','H','I']
plot_data = final.reindex(type_list, axis="columns")
plot_data_final = plot_data.reindex(type_list, axis="index")
plot_data_final = plot_data_final.fillna(0)

plot_data_final.to_csv('type2_9div_matrix_1552418101507.csv', encoding='utf-8')
plt.figure(figsize=(20,10))
ax = sns.heatmap(plot_data_final,cmap='Blues',xticklabels=True,yticklabels=True)
plt.savefig('Type2_9div_heatmap_1552418101507.png')

