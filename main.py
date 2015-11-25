# -*- coding: utf-8 -*-
from Module import text_from_request, url_from_text, rdf_from_url, similarity, information, most_referenced, \
    similar_result, targetedUriFromUrl
from flask import json
import time
import threading

'''
search : la requête de l'utilisateur
seuil : le seuil de similartié pour le graphe
type :  0 : actor
        1 : film
'''
def DoSearch(search, seuil, targetType):
    start = time.time()
    # googleRequestInFile = True

    # 0: subject,
    # 1: item,
    # 2: subjectAndItem
    requestType = 2

    # Module 1 - REQUEST -> URLs -> TEXT IN URLs
    jsonlist = Module1_GoogleAndAlchemy(search)

    # Module 2.1 - TEXT IN URLs -> URIs
    urllist = Module2_1_Spotlight(jsonlist)

    '''
    Appele le module 2 threader pour plus de rapidité et de cohérence

    Valeur de retour
    outThreads['mostReferenced'] = [None]
    outThreads['dbcontent'] = [None]
    outThreads['targetedUris'] = [None]
    '''
    outThreads = Module2_Threaded(urllist, targetType, requestType)

    # Thread le module 3 et le 4 ou 5
    # Matrice renvoyer par le module 3
    outMatrix = []
    # Retour module 4
    outTarget = [None]

    threads = []

    # Module 3 - [URL : graphe RDF] -> matrice similarté
    # t = threading.Thread(target=Module3, args=(outThreads['dbcontent'], outMatrix))
    # threads.append(t)
    # t.start()

    # On souhaite retrouvé quelque chose : on va donc afficher les informations que l'on a obtenus
    # Module 4 - [URI actor/film] -> information enrichies
    t = threading.Thread(target=Module4, args=(outThreads['targetedUris'], targetType, outTarget))
    threads.append(t)
    t.start()

    for t in threads:
        t.join()

    res = {}
    res["graph"] = {}  # module3_1.extractGraph(outMatrix, seuil)
    res["target"] = outTarget[0]

    print("Temps total : {0} sec".format(time.time() - start))
    return res

def Module2_Threaded(urllist, targetType, requestType):
    threads = []
    outThreads = {}
    outThreads['mostReferenced'] = [None]
    outThreads['dbcontent'] = [None]
    outThreads['targetedUris'] = [None]

    # What has been searched ?
    t = threading.Thread(target=FindMostReferenced, args=(urllist, targetType, outThreads))
    threads.append(t)
    t.start()

    # Module 2.2 - URIs -> DBPEDIA RDF GRAPHs
    t = threading.Thread(target=Module2_2_DBPedia, args=(urllist, requestType, outThreads))
    threads.append(t)
    t.start()

    # Module 2.3 - URIs -> DBPEDIA RDF GRAPHs
    t = threading.Thread(target=Module2_3_UriResource, args=(urllist, targetType, outThreads))
    threads.append(t)
    t.start()

    for t in threads:
        t.join()

    return outThreads

def Module1_GoogleAndAlchemy(searchKeyword):
    """
    Parameter : keywords to search for
    Query to google API so find 10 first URLs
    Send each link to Alchemy to extract text of page
    Return : A list of {'url': 'http://...', 'text': 'page content...'}
    """
    start = time.time()
    # subprocess.check_call(['./Module/module1.sh', search, '1'])
    pageResults = text_from_request.do_module1_job(searchKeyword)
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
    urlList = url_from_text.getUrlsFromTexts(jsonList)
    print("Module 2-1 (spotlight) : {0} sec".format(time.time() - start))
    return urlList

def Module2_2_DBPedia(urList, requestType, outThreads):
    start = time.time()
    outThreads['dbcontent'] = rdf_from_url.getRdfFromUrls(urList, requestType)
    print("Module 2-2 (dbpedia content) : {0} sec".format(time.time() - start))

def Module2_3_UriResource(urList, targetType, outThreads):
    start = time.time()
    dbpediaContent = targetedUriFromUrl.getTargetedUrisFromUrls(urList, targetType)
    print("Module 2-3 (targeted uri) : {0} sec".format(time.time() - start))
    outThreads['targetedUris']=  dbpediaContent

def Module3(grapheRDF, outMatrix):
    # call module 3 RDF TO RESULTS
    start = time.time()
    outMatrix = similarity.createSimilarityMatrix(grapheRDF)
    print("Module 3 : {0} sec".format(time.time() - start))


def Module4(setURI, targetType, outTarget):
    # call module 4 RDF TO RESULTS
    start = time.time()
    outTarget[0] = information.getInfoTargetFromUrls(setURI, targetType)
    print("Module 4 : {0} sec".format(time.time() - start))


def Module5(uri, targetType, ratio):
    # call module 5, one RDF TO similars RDFs
    start = time.time()
    similars = similar_result.getSimilar(uri, targetType, ratio)
    print("Module 5 : {0} sec".format(time.time() - start))
    return similars

'''
search : la requête de l'utilisateur
ratio : le seuil de similartié pour le graphe
type :  0 : actor
        1 : film
'''
def DoSimilar(search, ratio, type):
    # 0: subject,
    # 1: item,
    # 2: subjectAndItem
    requestType = 2

    # Module 1 - REQUEST -> URLs -> TEXT IN URLs
    jsonlist = Module1_GoogleAndAlchemy(search)

    # Module 2.1 - TEXT IN URLs -> URIs
    urllist = Module2_1_Spotlight(jsonlist)

    # What has been searched ?
    mostReferenced = FindMostReferenced(urllist, type)
    print(mostReferenced)
    similars = Module5(mostReferenced, type, ratio)
    print(similars)
    res = {'target':{}}
    for uri in similars:
        res['target'][uri] = information.getInfoTargetFromUrl(uri, type)
    return res


def FindMostReferenced(urlDic, elementType, outThreads):
    """
    Parameters :
        urlDic : Dictionnary : key = a URL, value = list of URIs
        elementType : 0 = movie, 1 = actor
    Returns : a URI
    """
    start = time.time()
    flatUriList = []
    for url in urlDic:
        for uri in urlDic[url]:
            flatUriList.append(uri)
    mostReferencedUri = most_referenced.findMostReferenced(flatUriList, 0)
    print("Most referenced : {0}".format(mostReferencedUri))
    print("Find most referenced : {0} sec".format(time.time() - start))
    outThreads['mostReferenced'] = mostReferencedUri


if __name__ == '__main__':
    # redirige l'output sur le fichier
    # sys.stdout = open('console.txt', 'w')

    # term = input()
    res = DoSearch("George actor", 0.3, 0)  # term)[1]))
    '''for k, v in res["target"].items():
        print(k.encode("utf-8", "ignore"))
        for key, value in v.items():
            print(key.encode("utf-8", "ignore"))
            print(value.encode("utf-8", "ignore"))
    '''
