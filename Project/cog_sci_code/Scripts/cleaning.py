import json
with open('interactions_1554476728882.json') as f:
	data = json.load(f)

print(len(data))

data_hover = [x for x in data if (x["customLogInfo"]["eventType"] == 'hover' and x["customLogInfo"]["elapsedTime"] < 0.1)]
data_calc = [x for x in data if x["customLogInfo"]["eventType"] == 'set_attribute_weight_vector_calc']
data_init = [x for x in data if x["customLogInfo"]["eventType"] == 'set_attribute_weight_vector_init']
data_select = [x for x in data if x["customLogInfo"]["eventType"] == 'set_attribute_weight_vector_select']
data_category = [x for x in data if x["customLogInfo"]["eventType"] == 'category_click']
data_help = [x for x in data if x["customLogInfo"]["eventType"] == 'help_hover']
data_att_drag = [x for x in data if x["customLogInfo"]["eventType"] == 'set_attribute_weight_vector_drag']
data_double = [x for x in data if x["customLogInfo"]["eventType"] == 'double_click']
data_cat_double = [x for x in data if x["customLogInfo"]["eventType"] == 'category_double_click']
data_drag = [x for x in data if (x["customLogInfo"]["eventType"] == 'drag' and x["customLogInfo"]["elapsedTime"] < 0.1)]
data_click = [x for x in data if x["customLogInfo"]["eventType"] == 'click']

eliminate_data = data_hover + data_calc + data_init + data_select + data_category + data_drag + data_help + data_att_drag + data_cat_double + data_double;
clean_data = [x for x in data if x not in eliminate_data]

print(len(clean_data))

with open('interactions_1554476728882_clean.json','w') as txtfile:
	json.dump(clean_data,txtfile,ensure_ascii=False)

#print(len(data_calc))
#print(len(data_init))
#print(len(data_select))
#print(len(data_category))
#print(len(data_help))
#print(len(data_att_drag))
#print(len(data_cat_double))
#print(len(data_double))
#print(len(data_hover))
#print(len(data_click))
#print(len(data_drag))