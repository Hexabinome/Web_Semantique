# ------------------------------------------
#           get_sparql_graph
# ------------------------------------------
from SPARQLWrapper import SPARQLWrapper, JSON

def getSparqlFromUrl(url):
  sparql = SPARQLWrapper("http://dbpedia.org/sparql")
  sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?label
    WHERE { <""" + url + """> ?e ?label }
  """)
  sparql.setReturnFormat(JSON)
  results = sparql.query().convert()
  return results



# from https://rdflib.github.io/sparqlwrapper/
## DEBUG
# results getSparqlFromUrl('http://dbpedia.org/resource/Asturias')
# print results
# for result in results["results"]["bindings"]:
#   print(result["label"]["value"])
## END of DEBUG