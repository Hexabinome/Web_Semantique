from Module import similarity, rdf_from_url

'''
    targetType 0 : actor
               1 : film
'''
def getSimilar(uri, targetType, ratio):
    # get rdf with items for this object
    rdf = rdf_from_url.getRdfFromUrl(uri, 2)
    # values est le graphe RDF contenant seulement les triplets qui on une
    # valeur
    if targetType == 1:
        values = [i for i in rdf if ('valeur' in i)]
    elif targetType == 0:
        values = [i for i in rdf if ('subject' in i)]
    vector = similarity.createSimilarityVector(values, targetType, ratio)
    return sorted(vector, key = vector.__getitem__, reverse = True)
