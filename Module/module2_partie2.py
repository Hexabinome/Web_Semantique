# -*- coding: utf-8 -*-
# ------------------------------------------
#           get_sparql_graph
# ------------------------------------------
from SPARQLWrapper import SPARQLWrapper, JSON
import json, threading

# TODO : Reflechir sur les requetes a effectuee
def getSparqlFromUrl(url):
    query = "SELECT * WHERE {{ <{0}> ?predicat ?valeur }}".format(url)
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    jsonResponse = sparql.query().convert()
    rdfTripletList = jsonResponse['results']['bindings']
    return json.dumps({url: rdfTripletList})

def getSparqlFromUrlThreaded(url, resultList, idx):
    resultList[idx] = getSparqlFromUrl(url)

'''
Launches a sparql query and returns a list of json objects.
'''
def getSparqlFromUrls(urlList):
    nbUrl = len(urlList)
    toReturn = [None] * nbUrl
    threads = [None] * nbUrl

    # Launch threads
    for i in range(nbUrl):
        threads[i] = threading.Thread(target=getSparqlFromUrlThreaded, args=(urlList[i], toReturn, i))
        threads[i].start()

    # Wait for threads
    for thread in threads:
        thread.join()
    return toReturn

# Example calls
#res = getSparqlFromUrl('http://dbpedia.org/resource/Beer') 
#results = getSparqlFromUrls(['http://dbpedia.org/resource/Beer', 'http://dbpedia.org/resource/Germany'])
