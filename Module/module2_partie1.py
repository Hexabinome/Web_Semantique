# ------------------------------------------
#           get_spotlight_uri
# ------------------------------------------
import requests, json, threading


# TODO: making the confidence and support changeable
def getUrlsFromText(jsonText):

    data = {'text' : jsonText,
        'confidence' : '0.2',
        'support' : '20' }

    url = 'http://spotlight.dbpedia.org/rest/annotate/'
    header = {'Accept' : 'application/json ', 'Content-Type' : 'application/json'}
    req = requests.post(url, data, headers=header)

    # TODO can throw error. Check status code 200
    jsonResponse = json.loads(req.text)

    urlList = []
    for resource in jsonResponse[u'Resources']:
        urlList.append(resource[u'@URI'])
    return urlList

def getUrlsFromTextThreaded(jsonTest, result, i):
    result[i] = getUrlsFromText(jsonTest)

def getUrlsFromTexts(jsonTexts):
    nbTexts = len(jsonTexts)
    allUrls = [None] * nbTexts
    threads = [None] * nbTexts;

    # Launch threads
    for i in range(nbTexts):
        threads[i] = threading.Thread(target=getUrlsFromTextThreaded, args=(jsonTexts[i]['text'], allUrls, i))
        threads[i].start()

    # Wait for threads
    for thread in threads:
        thread.join()

    return allUrls

# TEST
#print(getUrlFromText("""President Obama called Wednesday on Congress to extend a tax break
#    for students included in last year's economic stimulus package, arguing
#    that the policy provides more generous assistance."""))
#res = getUrlsFromTexts(["Berlin Germany beer Warsaw", """President Obama called Wednesday on Congress to extend a tax break
#    for students included in last year's economic stimulus package, arguing
#    that the policy provides more generous assistance."""])
