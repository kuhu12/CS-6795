import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
with open('interactions_1554476728882_clean.json') as f:
	data = json.load(f)

prev_value = ''
for i in data[:]:
	if(i['dataItem']['Name'] == prev_value):
		data.remove(i)
	else:
		prev_value = i['dataItem']['Name']


new_data=[]


for i in data:
	player_name = i['dataItem']['Name']
	data_loc = i['customLogInfo']['data_locations']
	quadrant = ''
	for q in data_loc:
		if q['player'] == player_name:
			if  (0 <= q['cx'] < 425) and (0 < q['cy'] <= 175):
				quadrant = 'A'
			elif (425 <= q['cx'] < 850) and (0 < q['cy'] <= 175):
				quadrant = 'B'
			elif (0 <= q['cx'] < 425) and (175 < q['cy'] <= 350):
				quadrant = 'C'
			else:
				quadrant = 'D'
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

quadrants=[]
size = len(new_data) -1

for i in new_data:
	quadrants.append(i['Quadrant'])

first = []
second =[]
for i in range(len(quadrants) - 1):
	first.append(quadrants[i])
	second.append(quadrants[i+1])

weight = [1]*size

matrix_ad = pd.DataFrame({'source': first, "target": second, 'weight': weight})
per = matrix_ad.groupby(["source","target"]).size().reset_index(name="weight")
final= per.pivot_table(index='source',columns='target',values='weight')
final = final.fillna(0)

type_list = ['A', 'B', 'C','D']
plot_data = final.reindex(type_list, axis="columns")
plot_data_final = plot_data.reindex(type_list, axis="index")

plot_data_final.to_csv('type1_4quad_matrix_1554476728882.csv', encoding='utf-8')
plt.figure(figsize=(20,10))
ax = sns.heatmap(plot_data_final,cmap='Blues',xticklabels=True,yticklabels=True)
plt.savefig('Type1_4quad_heatmap_1554476728882.png')

with open('interactions_4quad_1554476728882.json', 'w') as outfile:
    json.dump(new_data, outfile, sort_keys=True, indent=4)
