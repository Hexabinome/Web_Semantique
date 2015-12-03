# -*- coding: utf-8 -*-
# ------------------------------------------
# Get the most referenced uri from all the given one
# ------------------------------------------
from Module.sparql_helper import runQuery_returnBool

'''
Parametre : une liste de resources (uri), int pour le type rechercher (0 = film, 1 = acteur)
'''
def findMostReferenced(uriList, type):
    mostVisitedResources = {}

    # Uri les plus referencees
    for uri in uriList:
        incMap(mostVisitedResources, uri)

    isSomething = {0: isActor,
                   1: isMovie
                   }

    for uri in sorted(mostVisitedResources, key=mostVisitedResources.get, reverse=True):
        # print("{0}\t{1}".format(mostVisitedResources[uri], uri))
        if isSomething[type](uri):
            return uri

    return mostVisitedResources


def incMap(map, key):
    if key in map:
        map[key] += 1
    else:
        map[key] = 1


def isMovie(uri):
    query = "SELECT * WHERE {{ ?ok a dbo:Film. FILTER(?ok = <{0}>). }}".format(uri)
    return runQuery_returnBool(query)


def isActor(uri):
    # query = "SELECT DISTINCT ?ok WHERE {{ ?movie dbo:starring ?ok. FILTER(?ok = <{0}>). }}".format(uri)
    query = "SELECT ?ok WHERE {{ ?ok a <http://umbel.org/umbel/rc/Actor>. FILTER(?ok = <{0}>). }}".format(uri)
    return runQuery_returnBool(query)
