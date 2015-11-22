# ==========================
# Import
# ==========================
import os
import json
import pprint
import codecs
import sys
import time

# ==========================
# Déclaration variables
# ==========================

def createSimilarityMatrix(dbPedia): 
    sujetObjetsGraphes = {}

    # ==========================
    # Extraction du JSON
    # ==========================

    # Pour chaque page/url
    for url in dbPedia:
        sujetObjetsGraphes[url] = set()
        # Pour chaque uri dans cette page
        for uri in dbPedia[url]:
            # Pour chaque triplet dans cette uri
            for triplet in dbPedia[url][uri]:
                try:
                    sujet = triplet['subject']['value']
                except:
                    sujet = ''
                try:
                    predicat = triplet['predicat']['value']
                except:
                    predicat = ''
                try:
                    objet = triplet['valeur']['value']
                except:
                    objet = ''
    
                if sujet:
                    sujetObjetsGraphes[url].add(sujet)
                #if predicat:
                    #sujetObjetsGraphes[url].add(predicat)
                if objet:
                    sujetObjetsGraphes[url].add(objet)
        sujetObjetsGraphes[url] = list(sujetObjetsGraphes[url])

    # ==========================
    # Calcul de similarité
    # ==========================
    matriceIndice = {}

    # Calcul d'une moitié de la matrice
    nbLigne = 0
    for urlLigne in sujetObjetsGraphes:
        matriceIndice[urlLigne] = {}
        nbCol = -1
        for urlCol in sujetObjetsGraphes:
            nbCol += 1
            print('{2}\t{0}\t{1}'.format(urlLigne, urlCol, time.time()))
            if nbCol < nbLigne:
                matriceIndice[urlLigne][urlCol] = -1
                continue
            ratio = len([val for val in sujetObjetsGraphes[urlLigne] if val in sujetObjetsGraphes[urlCol]]) / (
                len(set(sujetObjetsGraphes[urlLigne] + sujetObjetsGraphes[urlCol])))
            matriceIndice[urlLigne][urlCol] = ratio
        nbLigne += 1

    # Duplication sur l'autre moitié de la matrice (un peu trop de duplication, un peu redondante, mais au final ça influe que peu)
    for urlCol in matriceIndice:
        for urlLigne in matriceIndice:
            matriceIndice[urlCol][urlLigne] = matriceIndice[urlLigne][urlCol]

    #print(matriceIndice)
    return matriceIndice

if __name__ == '__main__':
    createSimilarityMatrix()
