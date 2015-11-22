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

def createSimilarityMatrix(dpPedia): 
    sujetObjetsGraphes = list()
    ligneSujetObjetsGraphes = set()

    compteurSujetNull = 0
    #mon_fichier = open("dbpedia.json", "w") # Argh j'ai tout écrasé !
    #mon_fichier.write(json.dumps(dpPedia))
    #mon_fichier.close()

     # input_file=open('dbpedia.json', 'r', encoding='utf-8')
    with open('output.txt', 'w', encoding='utf-8') as f:

        # dpPedia=json.load(input_file)

        # ==========================
        # Extraction du JSON
        # ==========================

        # print(dpPedia)
        for listeGraphe in dpPedia:
            for graphe in listeGraphe:
                ligneSujetObjetsGraphes = set()
                for sujet in graphe:
                    # Le sujet n'a pas été retourné par dbpedia
                    if sujet == None:
                        break
                        # création d'un objet triplet pour retenir les résutats
                    triplet = {}
                    triplet['sujet'] = sujet

                    # On ajout le sujet dans la liste des sujet Objets du graphe en cours
                    try:
                        ligneSujetObjetsGraphes.add(sujet.encode('utf8'))
                    except:
                        ligneSujetObjetsGraphes.add(sujet)

                    for predicatSubject in graphe[sujet]:
                        if predicatSubject == None:
                            break

                        triplet['predicat'] = predicatSubject['predicat'].get('value')

                        # Parfois l'objet (predicatSubject['subject']) n'existe pas.
                        try:
                            triplet['objet'] = predicatSubject['subject'].get('value')

                            try:
                                ligneSujetObjetsGraphes.add(triplet['objet'].encode('utf8'))
                            except:
                                ligneSujetObjetsGraphes.add(triplet['objet'])
                        except:
                            compteurSujetNull += 1
                sujetObjetsGraphes.append(list(ligneSujetObjetsGraphes))
        # input_file.close()


        # ==========================
        # Calcul de similarité
        # ==========================

        matriceIndice = list()

        for iLigne in range(0, len(sujetObjetsGraphes)):
            ligneMatrice = list()
            for iCol in range(0, len(sujetObjetsGraphes)):
                ratio = len([val for val in sujetObjetsGraphes[iLigne] if val in sujetObjetsGraphes[iCol]]) / (
                len(list(set(sujetObjetsGraphes[iLigne] + sujetObjetsGraphes[iCol]))))
                ligneMatrice.append(ratio)
            matriceIndice.append(ligneMatrice)

        #print(matriceIndice)
        return matriceIndice
    input_file.close()

# Example calls TEST
# createSimilarityMatrix()