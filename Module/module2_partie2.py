# -*- coding: utf-8 -*-
# ------------------------------------------
#           get_sparql_graph
# ------------------------------------------
from SPARQLWrapper import SPARQLWrapper, JSON
import threading, json, os, ast

DIRECTORY = 'cache'

# TODO : Reflechir sur les requetes a effectuee
'''
requestType is a number to change the dbpedia query
'''
def getSparqlFromUrl(url, requestType):
    # ATTENTION. Si on modifie les requêtes associées aux indices, il faut supprimer (à la main) les fichiers en cache !!!
    options = {0: subject,
               1: item,
               2: subjectAndItem
               }

    cache_file = '{0}/{1}_{2}.txt'.format(DIRECTORY, url.replace('http://', '').replace('/', '_'), requestType)
    # Try finding url dbpedia content in cache
    if os.path.isfile(cache_file):
        cache_content = False
        with open(cache_file, 'r') as f:
            try:
                cache_content = ast.literal_eval(f.read())
                if len(cache_content[url]) == 0: # Not loaded correctly
                    cache_content = False
                else:
                    print("Loaded {0} from cache".format(cache_file))
            except:
                pass
        # If the cache_content is still false, remove existing invalid cache file + send request
        if not cache_content:
            os.remove(cache_file)
            return getSparqlFromUrl(url, requestType)
    # Else, query dbpedia
    else:
        query = options[requestType](url)
        cache_content = doQuery(url, query)

        # Save in cache
        if not os.path.exists(DIRECTORY):
            os.makedirs(DIRECTORY)
        try:
            with open(cache_file, 'w') as f:
                f.write(str(cache_content))
        except:
            #print('Cache writing error {0}'.format(cache_file))
            pass

    return cache_content

def doQuery(url, query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    jsonResponse = sparql.query().convert()
    rdfTripletList = jsonResponse['results']['bindings']
    return {url: json.loads(json.dumps(rdfTripletList))}

def testIsTargetType(url, target):
    options = {0: actor,
               1: film
            }
    query = options[target](url)
    return doQuery(url, query)[url]

def subject(url):
    request = "SELECT * WHERE {{ <{0}> ?predicat ?valeur}}".format(url)
    return request

def item(url):
    return "SELECT * WHERE {{  ?subject ?predicat <{0}> }}".format(url)

def subjectAndItem(url):
    return " SELECT * WHERE{{ {{ {0} }}UNION{{ {1} }} }}".format(item(url), subject(url))

def actor(url):
    return " SELECT ?acteur WHERE{{ {{ ?acteur a umbel-rc:Actor. FILTER(?acteur = <{0}>) }}UNION{{ ?film dbo:starring ?acteur. FILTER(?acteur = <{0}>) }} }}".format(url)

def film(url):
    return "SELECT * WHERE {{ ?a rdf:type ?????. FILTER(?a = <{0}>) } UNION {?film dbo:starring ?acteur. FILTER(?acteur = <{0}>)}}".format(url)


def getSparqlFromUrlThreaded(urls, resultUrlDict, resultTargetDict, requestType, target):
    for url in urls :
        resultUrlDict[url] = getSparqlFromUrl(url, requestType)
        if testIsTargetType(url, target) != []:
            resultTargetDict[url] = url

'''
Parameter is a list of urls.
Launches a sparql query for each different url
Returns a dictionnary like {'http://dbpedia.org/resource/Truc': 'jsonDBPediaContent'}
'''
def getSparqlFromUrls(listsOfUrls, requestType, target):
    # Copy urls in one set => unique elements
    urlDict = {}
    urlTab = []
    targetDict = {}
    for url in listsOfUrls:
        urlDict[url] = None
        urlTab.append(url)

    # storing threads
    threads = []

    size = len(urlTab)
    # Launch threads
    #while urlTab:
    for x in range(4):
        t = threading.Thread(target=getSparqlFromUrlThreaded, args=(urlTab[int(x*size/4):int((x+1)*size/4)], urlDict, targetDict, requestType, target))
        t.start()
        threads.append(t)
    # Wait for threads
    for t in threads:
        t.join()

    return urlDict

# Example calls TEST
# res = getSparqlFromUrl('http://dbpedia.org/resource/Beer', 1)

if __name__ == '__main__':
    results = getSparqlFromUrls(
      [['http://dbpedia.org/resource/Brad_Pitt'],
       ['http://dbpedia.org/resource/France'],
       ['http://dbpedia.org/resource/Angelina_Jolie'],
       ['http://dbpedia.org/resource/Brad_Davis_(actor)']], 0, 0)
    #results = getSparqlFromUrls(['http://dbpedia.org/resource/Beer', 'http://dbpedia.org/resource/Germany'], 0)
      # ['http://dbpedia.org/resource/Beer', 'http://dbpedia.org/resource/Germany', 'http://dbpedia.org/resource/Europe'],
      #  ['http://dbpedia.org/resource/France', 'http://dbpedia.org/resource/Baguette',
      #   'http://dbpedia.org/resource/Europe'], 0)
    print(results)
