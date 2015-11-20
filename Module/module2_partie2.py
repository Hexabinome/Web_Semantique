# -*- coding: utf-8 -*-
# ------------------------------------------
#           get_sparql_graph
# ------------------------------------------
from SPARQLWrapper import SPARQLWrapper, JSON
import threading, json

# TODO : Reflechir sur les requetes a effectuee
'''
requestType is a number to change the dbpedia query
'''
def getSparqlFromUrl(url, requestType):

    options = {0 : subject,
                1 : item,
                2 : subjectAndItem
    }
    query = options[requestType](url)
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    jsonResponse = sparql.query().convert()
    rdfTripletList = jsonResponse['results']['bindings']
    return {url: json.loads(json.dumps(rdfTripletList))}

def subject(url):
    return "SELECT * WHERE {{ <{0}> ?predicat ?valeur }}".format(url)

def item(url):
    return "SELECT * WHERE {{  ?subject ?predicat <{0}> }}".format(url)

def subjectAndItem(url):
    return " SELECT * WHERE{{ {{ {0} }}UNION{{ {1} }} }}".format(item(url), subject(url))

def getSparqlFromUrlThreaded(url, resultDict, requestType):
    resultDict[url] = getSparqlFromUrl(url, requestType)

'''
Parameter is a list of lists of urls. It
Launches a sparql query for each different url
Returns a list (of pages) of lists of jsonDBPediaContent
'''
def getSparqlFromUrls(listOfListsOfUrls, requestType):
    # Copy urls in one set => unique elements
    urlDict = {}
    for page in listOfListsOfUrls:
        if page:
            for url in page:
                urlDict[url] = None

    threads = []

    # Launch threads
    for url in urlDict.keys():
        t = threading.Thread(target=getSparqlFromUrlThreaded, args=(url, urlDict, requestType))
        t.start()
        threads.append(t)

    # Wait for threads
    for thread in threads:
        thread.join()

    # Create out list
    out_list = listOfListsOfUrls[:] # Realizes copy of elements
    for pageIdx in range(len(out_list)):
        if out_list[pageIdx]:
            for urlIdx in range(len(out_list[pageIdx])):
                url = out_list[pageIdx][urlIdx]
                out_list[pageIdx][urlIdx] = urlDict[url]

    return out_list

# Example calls
# res = getSparqlFromUrl('http://dbpedia.org/resource/Beer', 1)
# results = getSparqlFromUrls([['http://dbpedia.org/resource/Beer', 'http://dbpedia.org/resource/Germany', 'http://dbpedia.org/resource/Europe'],
#                            ['http://dbpedia.org/resource/France', 'http://dbpedia.org/resource/Baguette', 'http://dbpedia.org/resource/Europe']], 0)
# print(res)
