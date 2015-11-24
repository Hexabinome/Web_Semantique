# -*- coding: utf-8 -*-
from Module import module1, module2_partie1, module2_partie2, module3_1, module4, most_referenced
from flask import json
import time, threading


def DoSearch(search, seuil):
    # googleRequestInFile = True

    # TODO change requestType
    requestType = 2
    # TODO change targetList
    targetType = 0

    # Module 1 - REQUEST -> URLs -> TEXT IN URLs
    jsonlist = Module1_GoogleAndAlchemy(search)
    
    # Module 2.1 - TEXT IN URLs -> URIs
    urllist = Module2_1_Spotlight(jsonlist)

    # What has been searched ?
    mostReferenced = FindMostReferenced(urllist, 0) # Unused here

    # Module 2.2 - URIs -> DBPEDIA RDF GRAPHs
    dbcontent = Module2_2_DBPedia(urllist, requestType, targetType)

    #Thread le module 3 et 4
    #Matrice renvoyer par le module 3
    outMatrix = []
    #Retour module 4
    outTarget = []

    threads = []

    t = threading.Thread(target=Module3, args=(dbcontent['grapheRDF'], outMatrix))
    threads.append(t)
    t.start()

    t = threading.Thread(target=Module4, args=(dbcontent['setTarget'], targetType, outTarget))
    threads.append(t)
    t.start()

    for t in threads:
        t.join()

    res = {}
    res["graph"] = module3_1.extractGraph(outMatrix, seuil)
    res["target"] = outTarget
    return res

def Module1_GoogleAndAlchemy(searchKeyword):
    """
    Parameter : keywords to search for
    Query to google API so find 10 first URLs
    Send each link to Alchemy to extract text of page
    Return : A list of {'url': 'http://...', 'text': 'page content...'}
    """
    start = time.time()
    # subprocess.check_call(['./Module/module1.sh', search, '1'])
    pageResults = module1.do_module1_job(searchKeyword)
    dict = json.loads(pageResults)
    jsonlist = dict['resultats']
    print('Module 1 : {0} sec'.format(time.time() - start))

    return jsonlist

def Module2_1_Spotlight(jsonList):
    """
    Parameter : A list of {'url': 'http://...', 'text': 'page content...'}
    Sends for each url, the text to DBPedia Spotlight
    Return : A dictionnary where the key is a URL, and the value a list of URIs
    """
    start = time.time()
    urlList = module2_partie1.getUrlsFromTexts(jsonList)
    print("Module 2-1 (spotlight) : {0} sec".format(time.time() - start))
    return urlList

def Module2_2_DBPedia(urList, requestType, targetType):
    start = time.time()
    dbpediaContent = module2_partie2.getSparqlFromUrls(urList, requestType, targetType)
    print("Module 2-2 (dbpedia content) : {0} sec".format(time.time() - start))
    return dbpediaContent

def Module3(grapheRDF, outMatrix):
    # call module 3 RDF TO RESULTS
    start = time.time()
    outMatrix = module3_1.createSimilarityMatrix(grapheRDF)
    print("Module 3 : {0} sec".format(time.time() - start))

def Module4(setURI, targetType, outTarget):
    # call module 4 RDF TO RESULTS
    start = time.time()
    outTarget = module4.getInfoTargetFromUrls(setURI, targetType)
    print("Module 4 : {0} sec".format(time.time() - start))

def SearchLike(uri, searchType, ratio):
    rdf = module2_partie2.getInfoTargetFromUrls(uri, 0, 1)
    svector = createSimilarityVector(rdf, 'film', ratio)
    return svector

def FindMostReferenced(urlDic, elementType):
    """
    Parameters :
        urlDic : Dictionnary : key = a URL, value = list of URIs
        elementType : 0 = movie, 1 = actor
    Returns : a URI
    """
    start = time.time()
    flatUriList = []
    for url in urllist:
        for uri in urllist[url]:
            flatUriList.append(uri)
    mostReferencedUri = most_referenced.findMostReferenced(flatUriList, 0)
    print("Most referenced : {0}".format(mostReferencedUri))
    print("Find most referenced : {0} sec".format(time.time() - start))
    return mostReferencedUri

if __name__ == '__main__':
    # redirige l'output sur le fichier
    # sys.stdout = open('console.txt', 'w')

    # term = input()
    res = DoSearch("Brad actor", 0.3)  # term)[1]))
    for k, v in res["target"].items():
        print(k.encode("utf-8", "ignore"))
        for key, value in v.items():
            print(key.encode("utf-8", "ignore"))
            print(value.encode("utf-8", "ignore"))
