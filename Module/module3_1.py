# ==========================
# Import
# ==========================
import os 
import json
import pprint
import codecs
import sys
# ==========================
# Déclaration variables
# ==========================
graphes = list()
ligneGraphe = set()


def createSimilarityMatrix():#dpPedia):    
    #mon_fichier = open("dbpedia.json", "w") # Argh j'ai tout écrasé !
    #mon_fichier.write(json.dumps(dpPedia))
    #mon_fichier.close()

    input_file=open('dbpedia.json', 'r', encoding='utf-8')
    output_file=open('testoutput.json', 'w')
 
    dpPedia=json.load(input_file)

    # ==========================
    # Extraction du JSON
    # ==========================
    
    print(dpPedia)
    for graphe in dpPedia:
        print("graphe", graphe, "\n\n\n")
        for sujet in graphe:
            if sujet == None:   
                break 
            print("sujet ", sujet, "\n\n\n")

            triplet={}
            triplet['sujet']=sujet
            try:
                ligneGraphe.add(sujet.encode('utf8'))
            except:
                ligneGraphe.add(sujet)

            for predicat in graphe[sujet]:
                if predicat == None:   
                    break 
                triplet['predicat'] = predicat
                #print('predicat', predicat)
                for objet in graphe[sujet][predicat]:
                    if objet == None:   
                        break 

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

    return matriceIndice  