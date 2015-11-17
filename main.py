import subprocess
# from Module import module2_partie1
from flask import json

def DoSearch(search):
    # call module 1 REQUEST TO URL TO TEXT URL
    print('bash call')
    # subprocess.check_call(['./Module/module1.sh', search])
    print('bash end')
    f = open('Module/output/alchemy.json', 'r', encoding='utf-8')
    string = f.read()
    dict = json.loads(string)
    jsonlist = dict['resultats']
    # call module 2 TEXT URL TO URI TO RDF
    print('module 2 call')
    # module2_partie1.getUrlFromText(f.read())
    print('module 2 end')
    return 'rien'
    # call module 3 RDF TO RESULTS
