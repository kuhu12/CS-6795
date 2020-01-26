import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
with open('interactions_1554476728882_clean.json') as f:
	data = json.load(f)

players=[]
unique_list = []
size = len(data) -1

for i in data:
	players.append(i['dataItem']['Name'])

unique_list = list(set(players))
unique_list = unique_list.sort()

first = []
second =[]
for i in range(len(players) - 1):
	first.append(players[i])
	second.append(players[i+1])

weight = [1]*size

matrix_ad = pd.DataFrame({'source': first, "target": second, 'weight': weight})
per = matrix_ad.groupby(["source","target"]).size().reset_index(name="weight")
final= per.pivot_table(index='source',columns='target',values='weight')
final = final.fillna(0)
plot_data = pd.DataFrame(final, columns=unique_list)
plot_data.to_csv('type1_matrix_1554476728882.csv', encoding='utf-8')

plt.figure(figsize=(20,10))
ax = sns.heatmap(plot_data,cmap='Blues',xticklabels=True,yticklabels=True)
plt.savefig('Type1_heatmap_1554476728882.png')