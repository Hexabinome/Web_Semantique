# -*- coding: utf-8 -*-
# ------------------------------------------
#           get_sparql_graph
# ------------------------------------------
import threading
import os
from Module.sparql_helper import runQuery_returnBindings

CACHE_DIRECTORY = 'cache/uris/'


# TODO : Reflechir sur les requetes a effectuer

def testIsTargetType(url, target):
    options = {0: actor,
               1: film
               }

    query = options[target](url)
    uri = runQuery_returnBindings(query)
    return uri


def actor(url):
    return " SELECT ?acteur WHERE{{ {{ ?acteur a umbel-rc:Actor. FILTER(?acteur = <{0}>) }}UNION{{ ?film dbo:starring ?acteur. FILTER(?acteur = <{0}>) }} }}".format(
        url)


def film(url):
    return "SELECT DISTINCT ?film WHERE {{ {{?film a dbo:Film. FILTER(?film= <{0}>).}} UNION {{ ?film a <http://schema.org/Movie>. FILTER(?film= <{0}>).}} }}" \
        .format(url)


def getUriFromUrlThreaded(uris, targetSet, targetType, typeSet, nottypeSet):
    for uri in uris:
        if uri in typeSet:
            # already in cache of this type
            targetSet.add(uri)
        elif uri in nottypeSet:
            # already in cache of this not(type)
            nottypeSet.add(uri)
        elif testIsTargetType(uri, targetType) != []:
            targetSet.add(uri)
            typeSet.add(uri)
        else:
            nottypeSet.add(uri)


'''
Parameter is a dictionnary {url: [uri, uri, uri, ...], url: [...], ...}
Launches a sparql query for each different uri
Returns a set of targeted uri
targetType :
    0 : actor
    1 : film
'''


def getTargetedUrisFromUrls(urlDict, targetType):

    #GROSSE opti à faire ici pour faire 3 caches: film, acteur, autre
    if not os.path.exists(CACHE_DIRECTORY):
        os.makedirs(CACHE_DIRECTORY)
    cache_file = 'actor.json' if targetType == 0 else 'film.json'
    notcache_file = 'not'+cache_file
    cache_file = CACHE_DIRECTORY+cache_file
    notcache_file = CACHE_DIRECTORY+notcache_file
    # if cache files don't exist
    if not os.path.isfile(cache_file):
        open(cache_file, 'w').close()
    if not os.path.isfile(notcache_file):
        open(notcache_file, 'w').close()
    typeSet = set()
    nottypeSet = set()
    ori_typeSet = set()
    ori_nottypeSet = set()
    # load cache
    with open(cache_file, 'r') as cache:
        try:
            typeSet = set(cache.read().splitlines())
            ori_typeSet = typeSet.copy()
        except:
            pass
    with open(notcache_file, 'r') as notcache:
        try:
            nottypeSet = set(notcache.read().splitlines())
            ori_nottypeSet = nottypeSet.copy()
        except:
            pass

    # Contient toutes les uris acteurs ou films
    targetSet = set()
    # Contient toutes les uris
    uriSet = set()

    for url in urlDict:
        for uri in urlDict[url]:
            uriSet.add(uri)

    # storing threads
    threads = []

    nbURI = len(uriSet)
    nbThreads = min(4, nbURI)
    # Créer et lance les thread, qui vont appellé la méthode getSparqlFromUrlThreaded.
    # Chaque thread a un bout de la liste de toutes les url à traiter et les dictionnaires en entrée / sorties

    for x in range(nbThreads):
        t = threading.Thread(target=getUriFromUrlThreaded,
                             args=(
                                 list(uriSet)[int(x * nbURI / nbThreads):int((x + 1) * nbURI / nbThreads)],
                                 targetSet,
                                 targetType,
                                 typeSet,nottypeSet))
        t.start()
        threads.append(t)
    # Wait for threads
    for t in threads:
        t.join()
    # Update cache
    with open(cache_file, 'w') as cache:
        for uri in (typeSet-ori_typeSet):
            try:
                cache.write(uri+'\n')
            except:
                pass
    with open(notcache_file, 'w') as notcache:
        for uri in (nottypeSet-ori_nottypeSet):
            try:
                notcache.write(uri+'\n')
            except:
                pass
    return targetSet

#if __name__ == '__main__':
