from Module import similarity, rdf_from_url


def getSimilar(uri, targetType, ratio):
    # get rdf with items for this object
    rdf = rdf_from_url.getRdfFromUrl(uri, 1)
    similarity.createSimilarityVector(None, targetType, ratio)
