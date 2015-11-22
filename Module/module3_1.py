# ==========================
# Import
# ==========================
import os
import json
import pprint
import codecs
import sys
import time
import threading


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
                    # if predicat:
                    # sujetObjetsGraphes[url].add(predicat)
                if objet:
                    sujetObjetsGraphes[url].add(objet)
        sujetObjetsGraphes[url] = list(sujetObjetsGraphes[url])

    # ==========================
    # Calcul de similarité
    # ==========================
    matriceIndice = {}
    threads = []

    # Calcul d'une moitié de la matrice, 1 thread par URL
    for urlLigne in sujetObjetsGraphes:
        matriceIndice[urlLigne] = {}
        t = threading.Thread(target=ratioCalcThread, args=(matriceIndice, urlLigne, sujetObjetsGraphes))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # print(matriceIndice)
    return matriceIndice


def ratioCalcThread(resultMatrice, urlLigne, sujetObjetsGraphes):
    for urlCol in sujetObjetsGraphes:
        ratio = len([val for val in sujetObjetsGraphes[urlLigne] if val in sujetObjetsGraphes[urlCol]]) / (
            len(set(sujetObjetsGraphes[urlLigne] + sujetObjetsGraphes[urlCol])))
        resultMatrice[urlLigne][urlCol] = ratio
        print("{2}\t{0}\t{1}".format(urlLigne, urlCol, ratio))


if __name__ == '__main__':
    createSimilarityMatrix()
