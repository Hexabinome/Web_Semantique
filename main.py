# import subprocess
from Module import module1, module2_partie1, module2_partie2, module3_1, module4
from flask import json
import time, threading


def DoSearch(search, seuil):
    googleRequestInFile = True

    # TODO change requestType
    requestType = 2
    # TODO change targetList
    targetType = 0

    # call module 1 REQUEST TO URL TO TEXT URL
    print('Beginning')
    start = time.time()
    totalStart = time.time()
    # subprocess.check_call(['./Module/module1.sh', search, '1'])
    if googleRequestInFile == False:
        pageResults = module1.do_module1_job(search)
    print('Module 1 : {0} sec'.format(time.time() - start))


    if googleRequestInFile == False:
        with open('Module/output/alchemy_brad_pitt.json', 'a', encoding='utf-8') as f:
            f.write(pageResults)

        googleRequestInFile = True
        print("appelle google fait")
    else:
        with open('Module/output/alchemy_brad_pitt.json', 'r', encoding='utf-8') as f:
            pageResults = f.read()

    dict = json.loads(pageResults)
    jsonlist = dict['resultats']

    # call module 2 TEXT URL TO URI TO RDF
    start = time.time()
    urllist = module2_partie1.getUrlsFromTexts(jsonlist)

    print("Module 2 (spotlight) : {0} sec".format(time.time() - start))
    start = time.time()
    dbcontent = module2_partie2.getSparqlFromUrls(urllist, requestType, targetType)
    print("Module 2 (dbpedia content) : {0} sec".format(time.time() - start))

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

    print("Total time : {0} sec".format(time.time() - totalStart))

    res = {}
    res["graph"] = module3_1.extractGraph(outMatrix, seuil)
    res["target"] = outTarget
    return res

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
