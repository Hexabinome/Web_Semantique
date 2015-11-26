from SPARQLWrapper import SPARQLWrapper, JSON
import threading, json, sys, time, traceback

# ======================================================================================
#                         peuplateRdfFilms - Python script
#       This script is used to populate films.json with data from dbpedia
# First we have to all film important them we search for some predicats to compare films
# ======================================================================================


#  ====> retourne tous les films qui ont un budget, quelqu'il soit : 13 439 resultats url dbpedia de film
def getImportantFilm():
  return "SELECT DISTINCT ?description WHERE {?description rdf:type <http://dbpedia.org/ontology/Film>. ?description dbo:budget ?x.}"

# ======== Predicats choisis ========
# dbo:director
# dbo:distributor
# dbp:cinematography
# dct:subject
# dbo:musicComposer
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

#  launch a search and return: [predicat, cible]
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

# get the json from films.json as data
# for each line of allFilmsDbpedia launch the dbpedia query
# store the result in data {'fim':[[],[],[]], ...}
# /!\ when an error occured:
#  stored back the data as json
#  stored back the films not already searched
#  manually relaunch the script
def populate():
  # init
  data = {}
  predicatCibleTab = []
  sparql = SPARQLWrapper("http://live.dbpedia.org/sparql")
  sparql.setTimeout(2)
  sparql.setReturnFormat(JSON)

  #  load the current json file in data
  with open("data/films.json") as json_file:
    data = json.load(json_file)
  #  load the fils list from allFilmsDbpedia and delete the ones already compute
  filmsFile = open('data/allFilmsDbpedia', 'r+')
  lines = filmsFile.read().splitlines()

  # iterate over each line of allFilmsDbpedia
  lineCounter = 0
  for filmUri in lines:
    predicatCibleTab = []

    try:
      # ---- request director, distributor, cinematography,subject, musiccomposer -----
      predicatCibleTab.append(storePredicatTabToData(data, filmUri, 0,'director' ,sparql))
      predicatCibleTab.append(storePredicatTabToData(data, filmUri, 1,'distributor', sparql))
      # to avoid a lot of 502 http error
      time.sleep(2)
      predicatCibleTab.append(storePredicatTabToData(data, filmUri, 2,'cinematography', sparql))
      predicatCibleTab.append(storePredicatTabToData(data, filmUri, 3,'subject', sparql))
      time.sleep(2)
      predicatCibleTab.append(storePredicatTabToData(data, filmUri, 4,'musicComposer', sparql))
      time.sleep(1)

      #  add to dico
      data[filmUri] = predicatCibleTab
      lineCounter = lineCounter + 1

    # to handle 502 errors from dbpedia
    except Exception as e:
      print('__________________________DBPEDIA 502 ERROR ')
      # print(traceback.format_exc())
      #  rewrite the file of films minus the link already visited
      filmsFile = open('data/allFilmsDbpedia', 'w')
      for url in lines[lineCounter:]:
        if url != '\n':
          filmsFile.write(url)
          filmsFile.write('\n')
      # filmsFile.close()
      #  stocke the new json data with extra
      with open('data/films.json', 'r+') as outfile:
        json.dump(data, outfile)
      print('... you are getting an exception from dbpedia')
      print('your current work is stored, re-run script later')
      sys.exit()
  #  stocke the new json data with extra
  with open('data/films.json', 'r+') as outfile:
    json.dump(data, outfile)
  print('... you are done with work')


# First store all the films in a temporary file
def storeAllFilms():
  # init
  data = {}
  predicatCibleTab = []
  # sparql query to get all film
  query = getImportantFilm()
  sparql = SPARQLWrapper("http://live.dbpedia.org/sparql")
  sparql.setQuery(query)
  sparql.setTimeout(2)
  sparql.setReturnFormat(JSON)
  importantFilmJson = sparql.query().convert()

  f = open('data/allFilmsDbpedia', 'w')
  for x in importantFilmJson['results']['bindings']:
    # getting the url of the film
    filmUri = x['description']['value']
    f.write(filmUri)
    f.write('\n')
  f.close()



# =================== HOW TO USE ========================================
# First ypu have to store all disctinct film that have a budget (considered as important)
# storeAllFilms()
#  then you have to run  populate until allFilmsDbpedia is empty
populate()



