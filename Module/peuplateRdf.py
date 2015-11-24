from SPARQLWrapper import SPARQLWrapper, JSON
import threading, json, sys, time

# TODO : il faut faire des unions pour choisir parmis les films, les predicats important et utilisé pour la comparaison


# SELECT * WHERE {?description rdf:type <http://dbpedia.org/ontology/Film>.
#  ?description dbo:budget ?x.
# ?description dbo:director ?a.
# ?description dbo:distributor ?b.
# ?description dbp:cinematography ?c.
# ?description dct:subject ?d.
# ?description dbo:musicComposer ?e.
# }




#  ====> retourne tous les films qui ont un budget, quelqu'il soit : 13 439 resultats url dbpedia de film
def getImportantFilm():
  return "SELECT ?description WHERE {?description rdf:type <http://dbpedia.org/ontology/Film>. ?description dbo:budget ?x.}"

  # ======== Predicat choisits ========
  # dbo:director
  # dbo:distributor
  # dbp:cinematography
  # dct:subject
  # dbo:musicComposer
  #

def director(url):
  return "SELECT ?director WHERE {{<{0}> dbo:director ?director.}}".format(url)
def distributor(url):
  return "SELECT ?distributor WHERE {{<{0}> dbo:distributor ?distributor.}}".format(url)
def cinematography(url):
  return "SELECT ?cinematography WHERE {{<{0}> dbp:cinematography ?cinematography.}}".format(url)
def subject(url):
  return "SELECT ?subject WHERE {{<{0}> dct:subject ?subject.}}".format(url)
def musicComposer(url):
  return "SELECT ?musicComposer WHERE {{<{0}> dbo:musicComposer ?musicComposer.}}".format(url)
#  --------------

def storePredicatTabToData(data, filmUri, sparqlRequestNumber, predicat, sparql):
  innerTab = []

  options = {0: director,
             1: distributor,
             2: cinematography,
             3: subject,
             4: musicComposer
              }

  query = options[sparqlRequestNumber](filmUri)
  sparql.setQuery(query)
  sparql.setReturnFormat(JSON)
  triplet = sparql.query().convert()
  if (triplet['results']['bindings']):
    innerTab.append(predicat)
    innerTab.append(triplet['results']['bindings'][0][predicat]['value'])
    return innerTab


def populate():

  data = {}
  predicatCibleTab = []
  query = getImportantFilm()

  sparql = SPARQLWrapper("http://live.dbpedia.org/sparql")

  sparql.setQuery(query)
  sparql.setTimeout(2)
  sparql.setReturnFormat(JSON)
  importantFilmJson = sparql.query().convert()

  time.sleep(1)


  for x in importantFilmJson['results']['bindings']:
    # getting the url of the film
    filmUri = x['description']['value']

    # ---- request director, distributor, cinematography,subject, musiccomposer -----
    time.sleep(2)
    predicatCibleTab.append(storePredicatTabToData(data, filmUri, 0,'director' ,sparql))
    time.sleep(1)
    predicatCibleTab.append(storePredicatTabToData(data, filmUri, 1,'distributor', sparql))
    time.sleep(1)
    predicatCibleTab.append(storePredicatTabToData(data, filmUri, 2,'cinematography', sparql))
    time.sleep(1)
    predicatCibleTab.append(storePredicatTabToData(data, filmUri, 3,'subject', sparql))
    time.sleep(1)
    predicatCibleTab.append(storePredicatTabToData(data, filmUri, 4,'musicComposer', sparql))
    time.sleep(1)
    # ----------------------------

    #  add to dico
    data[filmUri] = predicatCibleTab
    predicatCibleTab = []



    print(json.dumps(data))

  return json.dumps(data)







print(populate())
# print(populate())


