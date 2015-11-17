# ==========================
# Import
# ==========================
import os 
import json
'''
# ==========================
# Extraction du JSON
# ==========================
input_file=open('testrdf.json', 'r')
output_file=open('testoutput.json', 'w')

json_decode=json.load(input_file)


result = []
for item in json_decode:
    my_dict={}
    my_dict['title']=item.get('labels').get('en').get('value')
    my_dict['description']=item.get('descriptions').get('en').get('value')
    my_dict['id']=item.get('id')
    print my_dict
    result.append(my_dict)

back_json=json.dumps(result, output_file)

output_file.write(back_json)
output_file.close() 
'''
# ==========================
# Calcul de similarité
# ==========================

tab = list()
ligne = list()

graphe = [
["yo1", "yo2", "yo3", "yo4"], 
["yo2", "yo5", "yo6", "yo7"],
["yo2", "yo3", "yo6", "yo7"]]

for iLigne in range(0,len(graphe)) :
    for iCol in range(0,len(graphe)) :
        ratio = len([val for val in graphe[iLigne] if val in graphe[iCol]]) / (len(list(set(graphe[iLigne] + graphe[iCol]))))
        ligne.append(ratio)
    tab.append(ligne)

print(tab)  

os.system("pause")