# -*- coding: utf-8 -*-
# ------------------------------------------
#           get_sparql_graph
# ------------------------------------------
from SPARQLWrapper import SPARQLWrapper, JSON
import threading, json, os, ast
import urllib

CACHE_DIRECTORY = 'cache/dbpedia'

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

    cache_file = '{0}/{1}_{2}.txt'.format(CACHE_DIRECTORY,
                                          url.replace('http://', '').replace('/', '_').replace(':', '_'), requestType)
    # Try finding url dbpedia content in cache
    if os.path.isfile(cache_file):
        cache_content = False
        with open(cache_file, 'r', encoding='utf-8') as f:
            try:
                cache_content = ast.literal_eval(ast.literal_eval(f.read()).decode('utf-8'))
                if len(cache_content[url]) == 0:  # Not loaded correctly
                    cache_content = False
                else:
                    #print("Loaded {0} from cache".format(cache_file))
                    pass
            except:
                pass
        # If the cache_content is still false, remove existing invalid cache file + send request
        if not cache_content:
            os.remove(cache_file)
            #print("Error cache loading {0}".format(cache_file))
            return getSparqlFromUrl(url, requestType)
    # Else, query dbpedia
    else:
        query = options[requestType](url)
        cache_content = doQuery(url, query)

        # Save in cache
        if not os.path.exists(CACHE_DIRECTORY):
            os.makedirs(CACHE_DIRECTORY)
        try:
            with open(cache_file, 'w') as f:
                f.write(str(str(cache_content).encode('utf-8')))
        except:
            #print('Cache writing error {0}'.format(cache_file))
            pass

    return cache_content


def doQuery(url, query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setTimeout(2)
    sparql.setReturnFormat(JSON)

    try:
        jsonResponse = sparql.query().convert()
        rdfTripletList = jsonResponse['results']['bindings']
    except urllib.error.URLError:
        rdfTripletList = [] # Timeout
    return json.loads(json.dumps(rdfTripletList))


def testIsTargetType(url, target):
    return []
    '''options = {0: actor,
               1: film
            }
    query = options[target](url)
    return doQuery(url, query)[url]'''


def subject(url):
    request = "SELECT * WHERE {{ <{0}> ?predicat ?valeur}}".format(url)
    return request


def item(url):
    return "SELECT * WHERE {{  ?subject ?predicat <{0}> }}".format(url)


def subjectAndItem(url):
    return " SELECT * WHERE{{ {{ {0} }}UNION{{ {1} }} }}".format(item(url), subject(url))


def actor(url):
    return " SELECT ?acteur WHERE{{ {{ ?acteur a umbel-rc:Actor. FILTER(?acteur = <{0}>) }}UNION{{ ?film dbo:starring ?acteur. FILTER(?acteur = <{0}>) }} }}".format(
        url)


def film(url):
    return "SELECT * WHERE {{ ?a rdf:type ?????. FILTER(?a = <{0}>) } UNION {?film dbo:starring ?acteur. FILTER(?acteur = <{0}>)}}".format(
        url)


def getSparqlFromUrlThreaded(uris, resultUrlDict, resultTargetDict, requestType, target):
    for uri in uris:
        resultUrlDict[uri] = getSparqlFromUrl(uri, requestType)
        if testIsTargetType(uri, target) != []:
            resultTargetDict[uri] = uri


'''
Parameter is a dictionnary {url: [uri, uri, uri, ...], url: [...], ...}
Launches a sparql query for each different uri
Returns dictionnary of a dictionnaries like {url: {uri: dbPedia, uri: dbpedia, uri:dbPedia...}, url: {...}, ...}
'''
def getSparqlFromUrls(urlDict, requestType, target):
    out_dict = {}
    uriSet = set()  # Copy URIs in one set => unique elements
    result_dict = {}
    targetDict = {}
    for url in urlDict:
        out_dict[url] = {}
        for uri in urlDict[url]:
            out_dict[url][uri] = None
            uriSet.add(uri)
            result_dict[uri] = None

    # storing threads
    threads = []

    size = len(uriSet)
    nbThreads = min(4, size)
    # Launch threads
    for x in range(nbThreads):
        t = threading.Thread(target=getSparqlFromUrlThreaded, args=(
        list(uriSet)[int(x * size / nbThreads):int((x + 1) * size / nbThreads)], result_dict, targetDict, requestType,
        target))
        t.start()
        threads.append(t)
    # Wait for threads
    for t in threads:
        t.join()

    # Fill out dict
    for url in out_dict:
        for uri in out_dict[url]:
            if uri in result_dict:
                out_dict[url][uri] = result_dict[uri]

    # print(targetDict)
    movieUri = findMostReferencedMovie(result_dict)

    res = {}
    res['grapheRDF'] = out_dict
    res['listeTarget'] = targetDict
    return res

'''
Paramètre : dictionnaire {uri: grapheRDF, uri: ...}
'''
def findMostReferencedMovie(dict):
    mostVisitedResources = {}
    for uri in dict:
        rdf = dict[uri]
        for triplet in rdf:

            pass

if __name__ == '__main__':
    results = getSparqlFromUrls(
        {'http://osef.org': ['http://dbpedia.org/resource/Brad_Pitt', 'http://dbpedia.org/resource/Angelina_Jolie'],
         'http://test.fr': ['http://dbpedia.org/resource/France', 'http://dbpedia.org/resource/Brad_Davis_(actor)',
                            'http://dbpedia.org/resource/Brad_Pitt']}
        , 0, 0)
    # results = getSparqlFromUrls(['http://dbpedia.org/resource/Beer', 'http://dbpedia.org/resource/Germany'], 0)
    # ['http://dbpedia.org/resource/Beer', 'http://dbpedia.org/resource/Germany', 'http://dbpedia.org/resource/Europe'],
    #  ['http://dbpedia.org/resource/France', 'http://dbpedia.org/resource/Baguette',
    #   'http://dbpedia.org/resource/Europe'], 0)
    print(results)



# results = getSparqlFromUrls(
#   [['http://dbpedia.org/resource/Brad_Pitt'],
#    ['http://dbpedia.org/resource/France'],
#    ['http://dbpedia.org/resource/Angelina_Jolie'],
