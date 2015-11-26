from SPARQLWrapper import SPARQLWrapper, JSON
import threading, json, sys, time, traceback

#  ====> retourne tous les acteurs qui ont un actors /!\ il faut filtrer les non-liens
def getImportantActor():
  return """select DISTINCT ?actor where  {
    ?film <http://dbpedia.org/property/label> ?k ;
       <http://dbpedia.org/property/starring> ?actor.
    }"""

# ======== Predicats choisis ========
# is dbo:starring of
# is dbo:producer of
def isStaringOf(url):
  return "SELECT ?starred WHERE {{?starred  dbo:starring   <{0}> .}}".format(url)
def isProducerOf(url):
  return "SELECT ?producer WHERE {{ ?producer dbo:producer  <{0}>.}}".format(url)

#  launch a search and return: [predicat, subject]
def storePredicatTabToData(data, filmUri, sparqlRequestNumber, predicat, sparql):
  innerTab = []

  options = {0: isStaringOf,
             1: isProducerOf
              }

  query = options[sparqlRequestNumber](filmUri)
  sparql.setQuery(query)
  sparql.setReturnFormat(JSON)
  triplet = sparql.query().convert()
  if (triplet['results']['bindings']):
    innerTab.append(predicat)
    innerTab.append(triplet['results']['bindings'][0][predicat]['value'])
    return innerTab

# get the json from actors.json as data
# for each line of allActorsDbpedia launch the dbpedia query
# store the result in data {'fim':[[],[],[]], ...}
# /!\ when an error occured:
#  stored back the data as json
#  stored back the actos not already searched
#  manually relaunch the script
def populate():
  # init
  data = {}
  predicatCibleTab = []
  sparql = SPARQLWrapper("http://live.dbpedia.org/sparql")
  sparql.setTimeout(10)
  sparql.setReturnFormat(JSON)

  #  load the current json file in data
  with open("data/actors.json") as json_file:
    data = json.load(json_file)
  #  load the fils list from allActorsDbpedia and delete the ones already compute
  actorsFile = open('data/allActorsDbpedia', 'r+')
  lines = actorsFile.read().splitlines()

  # iterate over each line of allActorsDbpedia
  lineCounter = 0
  for filmUri in lines:
    predicatCibleTab = []

    try:
      # ---- request director, distributor, cinematography,subject, musiccomposer -----
      time.sleep(1)
      predicatCibleTab.append(storePredicatTabToData(data, filmUri, 0,'starred' ,sparql))
      time.sleep(1)
      predicatCibleTab.append(storePredicatTabToData(data, filmUri, 1,'producer', sparql))
      # ----------------------------

      #  add to dico
      data[filmUri] = predicatCibleTab

      lineCounter = lineCounter + 1
      with open('data/actors.json', 'r+') as outfile:
        json.dump(data, outfile)


    # to handle 502 errors from dbpedia
    except Exception as e:
      print('__________________________DBPEDIA ERROR :')
      print(traceback.format_exc())
      #  rewrite the file of actors minus the link already visited
      actorsFile = open('data/allActorsDbpedia', 'w')
      for url in lines[lineCounter:]:
        if url != '\n':
          actorsFile.write(url)
          actorsFile.write('\n')
      # actorsFile.close()
      #  stocke the new json data with extra
      with open('data/actors.json', 'r+') as outfile:
        json.dump(data, outfile)
      print('... you are getting an exception from dbpedia')
      print('your current work is stored, re-run script later')
      sys.exit()

  # ========End of the work===========
  print('...Congratulation! Work is over !')

  with open('data/actors.json', 'r+') as outfile:
    json.dump(data, outfile)
  #  rewrite the file of actors minus the link already visited
  actorsFile = open('data/allActorsDbpedia', 'w')
  for url in lines[lineCounter:]:
    if url != '\n':
      actorsFile.write(url)
      actorsFile.write('\n')
  # actorsFile.close()



# First store all the actors
def storeAllActors():
  # init
  data = {}
  predicatCibleTab = []
  # sparql query to get all film
  query = getImportantActor()
  sparql = SPARQLWrapper("http://live.dbpedia.org/sparql")
  sparql.setQuery(query)
  sparql.setTimeout(2)
  sparql.setReturnFormat(JSON)
  importantFilmJson = sparql.query().convert()

  f = open('data/allActorsDbpedia', 'w')
  for x in importantFilmJson['results']['bindings']:
    # getting the url of the film
    if  x['actor']['type'] == 'uri':
      filmUri = x['actor']['value']
      f.write(filmUri)
      f.write('\n')



# =================== HOW TO USE ========================================
# First ypu have to store all disctinct actors that have a budget (considered as important)
# storeAllActors()
#  then you have to run  populate until allActorsDbpedia is empty
populate()



