# TODO : il faut faire des unions pour choisir parmis les films, les predicats important et utilisé pour la comparaison



#  ====> retourne tous les films qui ont un budget, quelqu'il soit : 13 439 resultats
# on peut utiliser le meme principes pour trier les films que l'on veut (un film nul dbpedia indique
 # meme pas le budget par exemple, meme si on le compare pas)
# SELECT count(?description) WHERE {?description rdf:type <http://dbpedia.org/ontology/Film>.
#                                   ?description dbo:budget  ?x. }



def getImportantFilm(url):
    return 'caca'