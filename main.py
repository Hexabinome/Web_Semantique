import subprocess
from Module import module2_partie1, module2_partie2
from flask import json


def DoSearch(search):
    # TODO change requestType
    requestType = 2
    # call module 1 REQUEST TO URL TO TEXT URL
    print('module 1 call')
    subprocess.check_call(['./Module/module1.sh', search])
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
    return dbcontent
    # call module 3 RDF TO RESULTS

if __name__ == '__main__':
    term = input()
    print(DoSearch(term))
