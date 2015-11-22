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

def createSimilarityMatrix(dpPedia): 
    sujetObjetsGraphes = list()
    ligneSujetObjetsGraphes = set()

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
    for urlLigne in sujetObjetsGraphes:
        matriceIndice[urlLigne] = {}
        for urlCol in sujetObjetsGraphes:
            ratio = len([val for val in sujetObjetsGraphes[urlLigne] if val in sujetObjetsGraphes[urlCol]]) / (
                len(set(sujetObjetsGraphes[urlLigne] + sujetObjetsGraphes[urlCol])))
            matriceIndice[urlLigne][urlCol] = ratio

    #print(matriceIndice)
    return matriceIndice

if __name__ == '__main__':
    createSimilarityMatrix()
