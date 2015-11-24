from Module import similarity, module2_partie2


def getSimilar(uri, targetType, ratio):
    # get rdf with items for this object
    rdf = module2_partie2.getRdfFromUrl(uri, 1)
    similarity.createSimilarityVector(None, targetType, ratio)
