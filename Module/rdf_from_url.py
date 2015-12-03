# -*- coding: utf-8 -*-
# ------------------------------------------
# Get the RDF graphes form a list of given uris
# ------------------------------------------
import threading
import os
import ast
from Module.sparql_helper import runQuery_returnBindings

CACHE_DIRECTORY = 'cache/dbpedia'

def getRdfFromUrl(url, requestType):
    # ATTENTION. Si on modifie les requêtes associées aux indices, il faut supprimer (à la main) les fichiers en cache !!!
    options = {0: subject,
               1: item,
               2: subjectAndItem
               }
    cache_file = '{0}/{1}_{2}.txt'.format(CACHE_DIRECTORY,
                                          url.replace('http://', '').replace('/', '_').replace(':', '_'), requestType)
    # Try finding url dbpedia content in cache
    if os.path.isfile(cache_file):
        # print('cache found')
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
            return getRdfFromUrl(url, requestType)
    # Else, query dbpedia
    else:
        # print("Query dbpedia {0}".format(url))
        query = options[requestType](url)
        # print(query)
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


def subject(url):
    request = "SELECT * WHERE {{ <{0}> ?predicat ?valeur}}".format(url)
    return request


def item(url):
    return "SELECT * WHERE {{  ?subject ?predicat <{0}> }}".format(url)


def subjectAndItem(url):
    return " SELECT * WHERE{{ {{ {0} }}UNION{{ {1} }} }}".format(item(url), subject(url))


def getRdfFromUrlThreaded(uris, resultUrlDict, requestType):
    for uri in uris:
        resultUrlDict[uri] = getRdfFromUrl(uri, requestType)


'''
Parameter is a dictionnary {url: [uri, uri, uri, ...], url: [...], ...}
Launches a sparql query for each different uri
Returns dictionnary of a dictionnaries like {url: {uri: dbPedia, uri: dbpedia, uri:dbPedia...}, url: {...}, ...}
requestType :
# 0: subject,
    # 1: item,
    # 2: subjectAndItem
'''


def getRdfFromUrls(urlDict, requestType):
    # key : url, valeur: graphe RDF
    out_dict = {}
    # Contient toutes les URIs
    uriSet = set()
    # Dictionnaire temporaire pour remplire ensuite out_dict
    result_dict = {}

    # créer des entrées dans les dictionnaire pour les toutes les uri
    # TODO Utile ?
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
    # Chaque thread a un bout de la liste de toutes les url à traiter et les dictionnaires en entrée / sorties
    for x in range(nbThreads):
        t = threading.Thread(target=getRdfFromUrlThreaded,
                             args=(
                                 list(uriSet)[int(x * nbURI / nbThreads):int((x + 1) * nbURI / nbThreads)],
                                 result_dict,
                                 requestType))
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

    return out_dict


if __name__ == '__main__':
    results = getRdfFromUrls(
        {'http://osef.org': ['http://dbpedia.org/resource/Brad_Pitt', 'http://dbpedia.org/resource/Angelina_Jolie'],
         'http://test.fr': ['http://dbpedia.org/resource/France', 'http://dbpedia.org/resource/Brad_Davis_(actor)',
                            'http://dbpedia.org/resource/Brad_Pitt']}
        , 0)

    print(results)
