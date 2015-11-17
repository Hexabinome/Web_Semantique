import subprocess
#from Module import module2_partie1


def DoSearch(search):
    # call module 1 REQUEST TO URL TO TEXT URL
    subprocess.check_call(['./Module/module1.sh', search])
    f = open('Module/output/alchemy.json')
    return f.read()
    # call module 2 TEXT URL TO URI TO RDF
    #module2_partie1.getUrlsFromText(f.read)
    # module2_partie2
    # call module 3 RDF TO RESULTS
