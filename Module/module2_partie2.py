# -*- coding: utf-8 -*-
# ------------------------------------------
#           get_sparql_graph
# ------------------------------------------
from SPARQLWrapper import SPARQLWrapper, JSON
import json

# TODO : Reflechir sur les requetes a effectuee
def getSparqlFromUrl(url):
    query = "SELECT * WHERE {{ <{0}> ?predicat ?valeur }}".format(url)
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    jsonResponse = sparql.query().convert()
    rdfTripletList = jsonResponse['results']['bindings']
    return json.dumps({url: rdfTripletList})

'''
Launches a sparql query and returns a list of json objects.
'''
def getSparqlFromUrls(urlList):
  toReturn = []
  for url in urlLisr:
    toReturn.append(getSparqlFromUrl(url))
  return toReturn

#res = getSparqlFromUrl('http://dbpedia.org/resource/Beer') # Call example
