# ------------------------------------------
#           get_spotlight_uri
# ------------------------------------------
import requests, json, threading, os

CACHE_DIRECTORY = 'cache/spotlight'


# TODO: making the confidence and support changeable
def getUrlsFromText(url, text, confidence, support):
    cache_file = '{0}/{1}_{2}_{3}.spotlight.txt'.format(CACHE_DIRECTORY,
                                                        url.replace('http://', '').replace('/', '_').replace(':',
                                                                                                             '_').replace(
                                                            '?', '_'),
                                                        confidence, support)
    # Try finding URIs in cache
    if os.path.isfile(cache_file):
        urlList = []
        with open(cache_file, 'r') as f:
            try:
                urlList = f.read().split('\n')
                # print("Loaded from {0} from cache".format(cache_file))
            except:
                pass
        # If the cache_content is still false, remove existing invalid cache file + send request
        if len(urlList) == 0:
            os.remove(cache_file)
            # print("Error loading cache {0}".format(cache_file))
            return getUrlsFromText(url, text, confidence, support)
    else:
        data = {
            'text': text,
            'confidence': confidence,
            'support': support}
        urlSpotlight = 'http://spotlight.dbpedia.org/rest/annotate/'
        header = {
            'Accept': 'application/json',
            'User-Agent':
                'Mozilla/5.0 (X11; Linux i686; rv:5.0) Gecko/20100101 Firefox/5.0'}

        try:
            req = requests.post(urlSpotlight, data, headers=header, timeout=3)
        except:
            # timeout exection
            return []

        # TODO can throw error. Check status code 200
        if req.status_code != 200:
            # raise IOError("ERR : {0}({1})\nJson was : {2}".format(req.reason, req.status_code, text))
            return []

        jsonResponse = json.loads(req.text)
        urlList = []
        try:
            for resource in jsonResponse[u'Resources']:
                urlList.append(resource[u'@URI'])
            # Save in cache
            if not os.path.exists(CACHE_DIRECTORY):
                os.makedirs(CACHE_DIRECTORY)
            try:
                with open(cache_file, 'w') as f:
                    f.write('\n'.join(urlList))
            except:
                # print('Cache writing error (spotlight) {0}'.format(cache_file))
                pass
        except:
            pass
    return urlList


def getUrlsFromTextThreaded(texts, result):
    for text in texts:
        if text['text'] != "":
            # TODO : make confidence & support changeable
            for uri in getUrlsFromText(text['url'], text['text'], 0.2, 20):
                if uri != []:
                    result[text['url']].add(uri)

'''
Parameter : list of dictionnaries, containing {'url':..., 'text':...}. Texts returned by Alchemy
Requests for each text DBPedia spotlight
Return : A dictionnary {url1: [foundUrl, foundUrl, ...], url2: [],...}
'''
def getUrlsFromTexts(jsonTexts):
    result = {}
    for dict in jsonTexts:
        result[dict['url']] = set()
    threads = []
    nbTexts = len(jsonTexts)
    # Launch threads
    nbThreads = min(5, nbTexts)
    for i in range(nbThreads):
        t = threading.Thread(
            target=getUrlsFromTextThreaded,
            args=(jsonTexts[int(i * nbTexts / nbThreads):int((i + 1) * nbTexts / nbThreads)], result))
        t.start()
        threads.append(t)

    # Wait for threads
    for thread in threads:
        thread.join()

    return result


if __name__ == '__main__':
    res = getUrlsFromTexts(
        [{'text': "Berlin Germany beer Warsaw", 'url': 'http://dbpedia.osef.org'}, {'url': 'coucou', 'text': """President Obama called Wednesday on Congress to extend a tax break
    for students included in last year's economic stimulus package, arguing
    that the policy provides more generous assistance."""}])
