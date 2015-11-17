# ==========================
# Import
# ==========================
import os 
import json
import pprint
import codecs
# ==========================
# Déclaration variables
# ==========================
graphes = list()
ligneGraphe = set()

# ==========================
# Extraction du JSON
# ==========================

input_file=open('06-papin-testrdf.json', 'r', encoding='utf-8')
output_file=open('testoutput.json', 'w')

json_decode=json.load(input_file)

#Pour l'instant c'est une page 
for graphe in json_decode:
    for sujet in graphe:
        triplet={}
        triplet['sujet']=sujet
        try:
            ligneGraphe.add(sujet.encode('utf8'))
        except:
            ligneGraphe.add(sujet)

        #print('sujet', sujet)
        for predicat in graphe[sujet]:
            triplet['predicat'] = predicat
            #print('predicat', predicat)
            for objet in graphe[sujet][predicat]:
                triplet['objet'] = objet.get('value')

                try:
                    ligneGraphe.add(objet.get('value').encode('utf8'))
                except:
                    ligneGraphe.add(objet.get('value'))

                #print('objet', objet.get('value'))
    graphes.append(list(ligneGraphe))

# ==========================
# Calcul de similarité
# ==========================

matriceIndice = list()

for iLigne in range(0,len(graphes)) :
    ligneMatrice = list() 
    for iCol in range(0,len(graphes)) :
        ratio = len([val for val in graphes[iLigne] if val in graphes[iCol]]) / (len(list(set(graphes[iLigne] + graphes[iCol]))))
        ligneMatrice.append(ratio)
    matriceIndice.append(ligneMatrice)

print(matriceIndice)  