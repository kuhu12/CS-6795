import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
with open('interactions_1554476728882_clean.json') as f:
	data = json.load(f)


new_data=[]


for i in data:
	player_name = i['dataItem']['Name']
	data_loc = i['customLogInfo']['data_locations']
	quadrant = ''
	for q in data_loc:
		if q['player'] == player_name:
			if  (0 <= q['cx'] < 212.5) and (0 <= q['cy'] < 87.5):
				quadrant = 'A'
			elif (212.5 <= q['cx'] < 425) and (0 <= q['cy'] < 87.5):
				quadrant = 'B'
			elif (425 <= q['cx'] < 637.5) and (0 <= q['cy'] < 87.5):
				quadrant = 'C'
			elif  (637.5 <= q['cx'] <= 850) and (0 <= q['cy'] < 87.5):
				quadrant = 'D'
			elif  (0 <= q['cx'] < 212.5) and (87.5 <= q['cy'] < 175):
				quadrant = 'E'
			elif (212.5 <= q['cx'] < 425) and (87.5 <= q['cy'] < 175):
				quadrant = 'F'
			elif (425 <= q['cx'] < 637.5) and (87.5 <= q['cy'] < 175):
				quadrant = 'G'
			elif  (637.5 <= q['cx'] <= 850) and (87.5 <= q['cy'] < 175):
				quadrant = 'H'
			elif  (0 <= q['cx'] < 212.5) and (175 <= q['cy'] < 262.5):
				quadrant = 'I'
			elif (212.5 <= q['cx'] < 425) and (175 <= q['cy'] < 262.5):
				quadrant = 'J'
			elif (425 <= q['cx'] < 637.5) and (175 <= q['cy'] < 262.5):
				quadrant = 'K'
			elif  (637.5 <= q['cx'] <= 850) and (175 <= q['cy'] < 262.5):
				quadrant = 'L'
			elif  (0 <= q['cx'] < 212.5) and (262.5 <= q['cy'] <= 350):
				quadrant = 'M'
			elif (212.5 <= q['cx'] < 425) and (262.5 <= q['cy'] <= 350):
				quadrant = 'N'
			elif (425 <= q['cx'] < 637.5) and (262.5 <= q['cy'] <= 350):
				quadrant = 'O'
			elif  (637.5 <= q['cx'] <= 850) and (262.5 <= q['cy'] <= 350):
				quadrant = 'P'

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

type_list = ['A', 'B', 'C','D','E','F','G','H','I','J','K','L','M','N','O','P']
plot_data = final.reindex(type_list, axis="columns")
plot_data_final = plot_data.reindex(type_list, axis="index")

plot_data_final.to_csv('type1_16div_matrix_1554476728882.csv', encoding='utf-8')
plt.figure(figsize=(20,10))
ax = sns.heatmap(plot_data_final,cmap='Blues',xticklabels=True,yticklabels=True)
plt.savefig('Type1_16div_heatmap_1554476728882.png')

with open('interactions_16div_1554476728882.json', 'w') as outfile:
    json.dump(new_data, outfile, sort_keys=True, indent=4)