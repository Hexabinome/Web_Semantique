# -*- coding: utf-8 -*-
# ------------------------------------------
#           get_sparql_graph
# ------------------------------------------
import threading, json, os, ast
import urllib
from Module.sparql_helper import runQuery_returnBindings

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
                if len(cache_content) == 0:  # Not loaded correctly
                    cache_content = False
                else:
                    # print("Loaded {0} from cache".format(cache_file))
                    pass
            except:
                pass
        # If the cache_content is still false, remove existing invalid cache file + send request
        if not cache_content:
            os.remove(cache_file)
            # print("Error cache loading {0}".format(cache_file))
            return getSparqlFromUrl(url, requestType)
    # Else, query dbpedia
    else:
        query = options[requestType](url)
        # print("Query dbpedia {0}".format(url))
        cache_content = runQuery_returnBindings(query)

        # Save in cache
        if not os.path.exists(CACHE_DIRECTORY):
            os.makedirs(CACHE_DIRECTORY)
        try:
            with open(cache_file, 'w') as f:
                f.write(str(str(cache_content).encode('utf-8')))
        except:
            # print('Cache writing error {0}'.format(cache_file))
            pass

    return cache_content

def testIsTargetType(url, target):
    options = {0: actor,
               1: film
            }
    query = options[target](url)
    return runQuery_returnBindings(query)


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
    return "SELECT DISTINCT ?film WHERE {{ {{?film a dbo:Film. FILTER(?film= <{0}>).}} UNION {{ ?film a <http://schema.org/Movie>. FILTER(?film= <{0}>).}} }}"\
        .format(url)


def getSparqlFromUrlThreaded(uris, resultUrlDict, targetSet, requestType, target):
    for uri in uris:
        #resultUrlDict[uri] = getSparqlFromUrl(uri, requestType)
        if testIsTargetType(uri, target) != []:
            targetSet.add(uri)

'''
Parameter is a dictionnary {url: [uri, uri, uri, ...], url: [...], ...}
Launches a sparql query for each different uri
Returns dictionnary of a dictionnaries like {url: {uri: dbPedia, uri: dbpedia, uri:dbPedia...}, url: {...}, ...}
requestType :
# 0: subject,
    # 1: item,
    # 2: subjectAndItem
targetType :
    0 : actor
    1 : film
'''
def getSparqlFromUrls(urlDict, requestType, targetType):
    #key : url, valeur: graphe RDF
    out_dict = {}
    # Contient toutes les URIs
    uriSet = set()
    #Dictionnaire temporaire pour remplire ensuite out_dict
    result_dict = {}

    #Contient tous les acteurs ou films
    targetSet = set()

    #créer des entrées dans les dictionnaire pour les toutes les uri
    #TODO Utile ?
    for url in urlDict:
        out_dict[url] = {}
        for uri in urlDict[url]:
            out_dict[url][uri] = None
            uriSet.add(uri)
            result_dict[uri] = None

    # storing threads
    threads = []

    nbURI = len(uriSet)
    nbThreads = min(4, nbURI)
    # Créer et lance les thread, qui vont appellé la méthode getSparqlFromUrlThreaded.
    #Chaque thread a un bout de la liste de toutes les url à traiter et les dictionnaires en entrée / sorties
    for x in range(nbThreads):
        t = threading.Thread(target=getSparqlFromUrlThreaded,
            args=(
                list(uriSet)[int(x * nbURI / nbThreads):int((x + 1) * nbURI / nbThreads)],
                result_dict,
                targetSet,
                requestType,
                targetType))
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

    res = {}
    res['grapheRDF'] = out_dict
    res['setTarget'] = targetSet
    print(targetSet)
    return res

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
