# import subprocess
from Module import module1, module2_partie1, module2_partie2, module3_1, module4
from flask import json
import sys, time


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
    if (googleRequestInFile == False):
        pageResults = module1.do_module1_job(search)
    print('Module 1 : {0} sec'.format(time.time() - start))

    if (googleRequestInFile == False):
        with open('Module/output/alchemy_brad_pitt.json', 'w', encoding='utf-8') as f:
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

    # call module 3 RDF TO RESULTS
    start = time.time()
    matrix = module3_1.createSimilarityMatrix(dbcontent['grapheRDF'])
    print("Module 3 : {0} sec".format(time.time() - start))

    # call module 4 RDF TO RESULTS
    start = time.time()
    target = module4.getInfoTargetFromUrls(
        # ['http://dbpedia.org/resource/Brad_Pitt', 'http://dbpedia.org/resource/Angelina_Jolie',
        # 'http://dbpedia.org/resource/Brad_Davis_(actor)'],0)
        ['http://dbpedia.org/resource/Interstellar_(film)',
         'http://dbpedia.org/resource/Pulp_Fiction'], 1)
    print("Module 4 : {0} sec".format(time.time() - start))

    print("Total time : {0} sec".format(time.time() - totalStart))

    res = {}
    res["graph"] = module3_1.extractGraph(matrix, seuil)
    res["target"] = target
    return res


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
