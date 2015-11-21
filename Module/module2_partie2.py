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
def getSparqlFromUrl(url, requestType):
    options = {0: subject,
               1: item,
               2: subjectAndItem
               }
    query = options[requestType](url)
    return doQuery(url, query)

def testIsTargetType(url, target):
    options = {0: actor,
               1: film
            }
    query = options[target](url)
    return doQuery(url, query)[url]

def doQuery(url, query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    jsonResponse = sparql.query().convert()
    rdfTripletList = jsonResponse['results']['bindings']
    return {url: json.loads(json.dumps(rdfTripletList))}

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
    for x in range(0, 3):
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
