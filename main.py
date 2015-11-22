import subprocess
from Module import module1, module2_partie1, module2_partie2, module3_1
from flask import json
import sys, time


def DoSearch(search):
    # TODO change requestType
    requestType = 2
    # call module 1 REQUEST TO URL TO TEXT URL
    print('Beginning')
    start = time.time()
    totalStart = time.time()
    #subprocess.check_call(['./Module/module1.sh', search, '1'])
    pageResults = module1.do_module1_job(search)
    print('Module 1 : {0} sec'.format(time.time() - start))

    #with open('Module/output/alchemy_brad_pitt.json', 'r', encoding='utf-8') as f:
    #    pageResults = f.read()
    dict = json.loads(pageResults)
    jsonlist = dict['resultats']

    # call module 2 TEXT URL TO URI TO RDF
    start = time.time()
    urllist = module2_partie1.getUrlsFromTexts(jsonlist)
    print(urllist)
    print("Module 2 (spotlight) : {0} sec".format(time.time() - start))
    start = time.time()
    dbcontent = module2_partie2.getSparqlFromUrls(urllist, requestType)
    print("Module 2 (dbpedia content) : {0} sec".format(time.time() - start))

    # call module 3 RDF TO RESULTS
    start = time.time()
    matrix = module3_1.createSimilarityMatrix(dbcontent)
    print("Module 3 : {0} sec".format(time.time() - start))
    print("Total time : {0} sec".format(time.time() - totalStart))

    return matrix

if __name__ == '__main__':
    # redirige l'output sur le fichier
    #sys.stdout = open('console.txt', 'w')

    #term = input()
    print((DoSearch("plane")))#term)[1]))
