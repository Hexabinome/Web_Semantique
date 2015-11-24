# -*- coding: utf-8 -*-
# ------------------------------------------
#           get_sparql_graph
# ------------------------------------------
from SPARQLWrapper import SPARQLWrapper, JSON
import threading, json, sys

# TODO : Reflechir sur les requetes a effectuee
'''
requestType is a number to change the dbpedia query
'''


def getInfoFromUrl(url, targetType):
    # actors
    resultDict = {}
    if targetType == 0:
        # Actors
        resultDict['resume'] = doQuery(url, resume(url))
        resultDict['birth'] = doQuery(url, birthDate(url))
        resultDict['thumbnail'] = doQuery(url, thumbnail(url))
        resultDict['alias'] = doQuery(url, alias(url))
    elif targetType == 1:
        # Films
        resultDict['runtime'] = doQuery(url, runtime(url))
        resultDict['budget'] = doQuery(url, budget(url))
        resultDict['director'] = doQuery(url, director(url))
        resultDict['comment'] = doQuery(url, comment(url))
        resultDict['name'] = doQuery(url, name(url))
    return resultDict


def doQuery(url, query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    jsonResponse = sparql.query().convert()
    rdfTripletList = jsonResponse['results']['bindings'][0].popitem()[1]['value']
    if isinstance(rdfTripletList, str):
        rdfTripletList = rdfTripletList.replace('"', "'")
    return json.loads(json.dumps(rdfTripletList))


def resume(url):
    return "SELECT ?resume WHERE {{<{0}> dbo:abstract ?resume. FILTER (lang(?resume) = 'en')}}".format(url)


def birthDate(url):
    return "SELECT ?birth WHERE {{<{0}> dbo:birthDate ?birth .}}".format(url)


def thumbnail(url):
    return "SELECT ?thumbnail WHERE {{<{0}> dbo:thumbnail ?thumbnail .}}".format(url)


def alias(url):
    return "SELECT ?alias WHERE {{<{0}> dbo:alias ?alias. FILTER (lang(?alias ) = 'en')}}".format(url)


def runtime(url):
    return "SELECT ?runtime WHERE {{<{0}> dbo:runtime ?runtime.}}".format(url)


def budget(url):
    return "SELECT ?budget WHERE {{<{0}> dbp:budget ?budget.}}".format(url)


def director(url):
    return "SELECT ?director WHERE {{<{0}> dbo:director ?director.}}".format(url)


def name(url):
    return "SELECT ?name WHERE {{<{0}> dbp:name ?name.}}".format(url)


def comment(url):
    return "SELECT ?comment WHERE {{<{0}> dbo:abstract ?comment. FILTER (lang(?comment)='en')}}".format(url)


def getInfoFromUrlThreaded(urls, resultDict, targetType):
    for url in urls:
        resultDict[url] = getInfoFromUrl(url, targetType)


'''
Parameter is a list of lists of urls. It
Launches a sparql query for each different url
Returns a list (of pages) of lists of jsonDBPediaContent
'''


def getInfoTargetFromUrls(listOfUrls, targetType):
    # Copy urls in one set => unique elements
    resDict = {}

    # storing threads
    threads = []

    size = len(listOfUrls)
    # Launch threads
    if (size < 5):
        for x in range(0, size):
            t = threading.Thread(target=getInfoFromUrlThreaded, args=([listOfUrls[x]], resDict, targetType))
            t.start()
            threads.append(t)
    else:
        for x in range(0, 3):
            t = threading.Thread(target=getInfoFromUrlThreaded,
                                 args=(listOfUrls[int(x * size / 4):int((x + 1) * size / 4)], resDict, targetType))
            t.start()
            threads.append(t)
    # Wait for threads
    for t in threads:
        t.join()

    return resDict


    # Example calls TEST
    # res = getSparqlFromUrl('http://dbpedia.org/resource/Beer', 1)
    # redirige l'output sur le fichier
    # sys.stdout = open('console.txt', 'w', encoding="utf-8")

    # results = getInfoTargetFromUrls(
    #   ['http://dbpedia.org/resource/Brad_Pitt',
    #    'http://dbpedia.org/resource/Angelina_Jolie',
    #    'http://dbpedia.org/resource/Brad_Davis_(actor)'], 0)
    # print(results)
