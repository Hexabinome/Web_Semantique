import subprocess
from Module import module2_partie1, module2_partie2, module3_1, module4
import json
import sys

def DoSearch(search):
    # TODO change requestType
    requestType = 2
    # TODO change targetList
    targetType = 0
    # call module 1 REQUEST TO URL TO TEXT URL
    print('module 1 call')
    #subprocess.check_call(['./Module/module1.sh', search, '1'])
    print('module 1 end')

    with open('Module/output/alchemy_brad_pitt.json', 'r', encoding='utf-8') as f:
        string = f.read()
    dict = json.loads(string)
    jsonlist = dict['resultats']

    # call module 2 TEXT URL TO URI TO RDF
    print('module 2 call')
    urllist = module2_partie1.getUrlsFromTexts(jsonlist)
    dbcontent = module2_partie2.getSparqlFromUrls(urllist, requestType, targetType)
    print('module 2 end')
    # return dbcontent

    # call module 3 RDF TO RESULTS
    print('module 3 call')
    matrix = module3_1.createSimilarityMatrix(dbcontent['grapheRDF'])
    print('module 3 end')

    res = {}
    res["matrice"] = matrix
    res["target"] = module4.getInfoTargetFromUrls(['http://dbpedia.org/resource/Brad_Pitt',   'http://dbpedia.org/resource/Angelina_Jolie',   'http://dbpedia.org/resource/Brad_Davis_(actor)'], 0) #list(dbcontent['listeTarget'].keys()), 0)
    print(json.dumps(res["target"]))
    return res

if __name__ == '__main__':
    # redirige l'output sur le fichier
    sys.stdout = open('console.txt', 'w')

    #term = input()
    DoSearch("")#term)[1]))
