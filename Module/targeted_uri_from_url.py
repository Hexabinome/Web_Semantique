﻿# -*- coding: utf-8 -*-
# ------------------------------------------
#           get_sparql_graph
# ------------------------------------------
import threading
from Module.sparql_helper import runQuery_returnBindings

CACHE_DIRECTORY = 'cache/dbpedia'


# TODO : Reflechir sur les requetes a effectuee

def testIsTargetType(url, target):
    options = {0: actor,
               1: film
               }
    query = options[target](url)
    return runQuery_returnBindings(query)


def actor(url):
    return " SELECT ?acteur WHERE{{ {{ ?acteur a umbel-rc:Actor. FILTER(?acteur = <{0}>) }}UNION{{ ?film dbo:starring ?acteur. FILTER(?acteur = <{0}>) }} }}".format(
        url)


def film(url):
    return "SELECT DISTINCT ?film WHERE {{ {{?film a dbo:Film. FILTER(?film= <{0}>).}} UNION {{ ?film a <http://schema.org/Movie>. FILTER(?film= <{0}>).}} UNION {{ ?film a umbel-rc:Movie_CW. FILTER(?film= <{0}>).}} UNION {{ ?film a umbel-rc:Movie_CW. FILTER(?film= <{0}>).}} }}" \
        .format(url)


def getUriFromUrlThreaded(uris, targetSet, targetType):
    for uri in uris:
        if testIsTargetType(uri, targetType) != []:
            targetSet.add(uri)

'''
Parameter is a dictionnary {url: [uri, uri, uri, ...], url: [...], ...}
Launches a sparql query for each different uri
Returns a set of targeted uri
targetType :
    0 : actor
    1 : film
'''
def getTargetedUrisFromUrls(urlDict, targetType):
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
                                 targetType))
        t.start()
        threads.append(t)
    # Wait for threads
    for t in threads:
        t.join()

    print(targetSet)
    return targetSet

#if __name__ == '__main__':
