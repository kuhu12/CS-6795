import json
with open('interactions_1553883152091.json') as f:
	data = json.load(f)

interactions = []
for j in data:
	interactions.append(j['customLogInfo']['eventType'])

print(set(interactions))
