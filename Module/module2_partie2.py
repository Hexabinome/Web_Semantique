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

def getSparqlFromUrlThreaded(url, resultDict):
    resultDict[url] = getSparqlFromUrl(url)

'''
Parameter is a list of lists of urls. It 
Launches a sparql query for each different url
Returns a list (of pages) of lists of jsonDBPediaContent
'''
def getSparqlFromUrls(listOfListsOfUrls):
    # Copy urls in one set => unique elements
    urlDict = {}
    for page in listOfListsOfUrls:
        for url in page:
            urlDict[url] = None

    threads = []
    
    # Launch threads
    for url in urlDict.keys():
        t = threading.Thread(target=getSparqlFromUrlThreaded, args=(url, urlDict))
        t.start()
        threads.append(t)

    # Wait for threads
    for thread in threads:
        thread.join()

    # Create out list
    out_list = listOfListsOfUrls[:] # Realizes copy of elements
    for pageIdx in range(len(out_list)):
        for urlIdx in range(len(out_list[pageIdx])):
            url = out_list[pageIdx][urlIdx]
            out_list[pageIdx][urlIdx] = urlDict[url]

    return out_list

# Example calls
#res = getSparqlFromUrl('http://dbpedia.org/resource/Beer') 
#results = getSparqlFromUrls([['http://dbpedia.org/resource/Beer', 'http://dbpedia.org/resource/Germany', 'http://dbpedia.org/resource/Europe'],
#                            ['http://dbpedia.org/resource/France', 'http://dbpedia.org/resource/Baguette', 'http://dbpedia.org/resource/Europe']])
