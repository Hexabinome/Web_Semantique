# ==========================
# Import
# ==========================
import threading
import json


# ==========================
# Déclaration variables
# ==========================
def createSimilarityVector(filmRDF, searchType, ratio):
    similarityVector = {}
    if searchType == 0:
        with open('Data/films.json', 'r') as f:
            allData = json.loads(f.read())
    elif searchType == 1:
        with open('Data/actors.json', 'r') as f:
            allData = json.loads(f.read())
    else:
        return {}
    for uri in allData:
        actualRatio = similarity(filmRDF, allData[uri], searchType)
        #TODO enlever quand on compare un acteur avec lui même
        if actualRatio >= ratio:
            similarityVector[uri] = actualRatio
    return similarityVector


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
    urlTab = []
    for urlLigne in sujetObjetsGraphes:
        urlTab.append(urlLigne)

    # Calcul d'une moitié de la matrice, 1 thread par URL
    for idxLigne in range(len(urlTab)):
        matriceIndice[urlTab[idxLigne]] = {}
        t = threading.Thread(target=ratioCalcThread, args=(matriceIndice, urlTab, idxLigne, sujetObjetsGraphes))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Copy results of matrix
    for idxCol in range(len(urlTab)):
        for idxLigne in range(idxCol + 1, len(urlTab)):
            matriceIndice[urlTab[idxLigne]][urlTab[idxCol]] = matriceIndice[urlTab[idxCol]][urlTab[idxLigne]]

    for idxCol in range(len(urlTab)):
        for idxLigne in range(len(urlTab)):
            print(urlTab[idxLigne], urlTab[idxCol], matriceIndice[urlTab[idxLigne]][urlTab[idxCol]])

    return matriceIndice


def similarity(RDF1, RDF2, type):
    value = 'valeur' if type == 0 else 'subject'
    common = 0
    initLen = len(RDF2)
    for i in RDF1:
        #print(i)
        for j in RDF2:
            #print(j)
            if not j:
                continue
            if(i[value]['value'] == j[1]):
                common += 1
                RDF2.remove(j)
    print(common/initLen)
    return common/initLen


def ratioCalcThread(resultMatrice, urlTab, idxLigne, sujetObjetsGraphes):
    for idxCol in range(idxLigne, len(urlTab)):
        urlLigne = urlTab[idxLigne]
        urlCol = urlTab[idxCol]
        if idxLigne == idxCol:
            ratio = 1.0
        else:
            try:
                ratio = len([val for val in sujetObjetsGraphes[urlLigne] if val in sujetObjetsGraphes[urlCol]]) / (
                    len(set(sujetObjetsGraphes[urlLigne] + sujetObjetsGraphes[urlCol])))
            except ZeroDivisionError:
                ratio = 0

        resultMatrice[urlLigne][urlCol] = ratio


def extractGraph(matrice, seuil):
    graph = {}

    for urlCol in matrice:
        graph[urlCol] = []
        for urlLigne in matrice[urlCol]:
            if ((matrice[urlCol][urlLigne] > seuil) or (matrice[urlCol][urlLigne] != 1)):
                graph[urlCol].append(urlLigne)

    return graph


if __name__ == '__main__':
    createSimilarityMatrix()
