# -*- coding: utf-8 -*-
from SPARQLWrapper import SPARQLWrapper, JSON
import json

def runQuery_returnBool(query):
    return len(runQuery) != 0

def runQuery_returnBindins(query):
    return json.loads(json.dumps(runQuery(runQuery)))

def runQuery(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setTimeout(3)
    sparql.setReturnFormat(JSON)

    try:
        jsonResponse = sparql.query().convert()
        rdfTripletList = jsonResponse['results']['bindings']
    except:
        rdfTripletList = [] # Timeout

    return rdfTripletList
