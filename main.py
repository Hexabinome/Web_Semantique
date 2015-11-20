import subprocess
from Module import module2_partie1, module2_partie2, module3_1
from flask import json
import sys

def DoSearch(search):
    # TODO change requestType
    requestType = 2
    # call module 1 REQUEST TO URL TO TEXT URL
    print('module 1 call')
    subprocess.check_call(['./Module/module1.sh', search, '1'])
    print('module 1 end')

    with open('Module/output/alchemy.json', 'r', encoding='utf-8') as f:
        string = f.read()
    dict = json.loads(string)
    jsonlist = dict['resultats']
    # call module 2 TEXT URL TO URI TO RDF
    print('module 2 call')
    urllist = module2_partie1.getUrlsFromTexts(jsonlist)
    dbcontent = module2_partie2.getSparqlFromUrls(urllist, requestType)
    print('module 2 end')
    #return dbcontent

    #call module 3 RDF TO RESULTS
    print('module 3 call')
    matrix = module3_1.createSimilarityMatrix()#dbcontent)
    print('module 3 end')

    return matrix
if __name__ == '__main__':
    #redirige l'output sur le fichier
    sys.stdout = open('console.txt', 'w')

    term = input()
    print((DoSearch(term)[1]))
