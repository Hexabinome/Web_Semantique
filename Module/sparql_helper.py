# -*- coding: utf-8 -*-
from SPARQLWrapper import SPARQLWrapper, JSON
import json


def runQuery_returnBool(query):
    return len(runQuery(query)) != 0


def runQuery_returnBindings(query):
    return json.loads(json.dumps(runQuery(query)))

def runQuery(query, timeout=2):
    sparql = SPARQLWrapper("http://live.dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setTimeout(timeout)
    sparql.setReturnFormat(JSON)

    try:
        jsonResponse = sparql.query().convert()
        rdfTripletList = jsonResponse['results']['bindings']
    except:
        rdfTripletList = []  # Timeout

    return rdfTripletList
