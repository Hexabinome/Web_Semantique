# ------------------------------------------
#           get_spotlight_uri
# ------------------------------------------
import requests
import json
import threading


# TODO: making the confidence and support changeable
def getUrlsFromText(text):
    data = {
        'text': text,
        'confidence': '0.2',
        'support': '20'}
    url = 'http://spotlight.dbpedia.org/rest/annotate/'
    header = {
        'Accept': 'application/json',
        'User-Agent':
            'Mozilla/5.0 (X11; Linux i686; rv:5.0) Gecko/20100101 Firefox/5.0'}

    req = requests.post(url, data, headers=header)

    # TODO can throw error. Check status code 200
    if req.status_code != 200:
        raise IOError("ERR : {0}({1})\nJson was : {2}".format(req.reason, req.status_code, text))
    jsonResponse = json.loads(req.text)
    # print(jsonResponse.keys())
    urlList = []
    for resource in jsonResponse[u'Resources']:
        urlList.append(resource[u'@URI'])
    return deleteDoublonFromUrlList(urlList)


def getUrlsFromTextThreaded(texts, result):
    for text in texts:
        for url in getUrlsFromText(text['text']):
            result.add(url)

'''
Parameter : list of dictionnaries, containing {'url':..., 'text':...}. Texts returned by Alchemy
Requests for each text DBPedia spotlight
Return : A list of all urls found in the different texts
'''
def getUrlsFromTexts(jsonTexts):
    nbTexts = len(jsonTexts)
    allUrls = set()
    threads = []
    # Launch threads
    nbThreads = min(5, nbTexts)
    for i in range(nbThreads):
        t = threading.Thread(
            target=getUrlsFromTextThreaded,
            args=(jsonTexts[int(i*nbTexts/nbThreads):int((i+1)*nbTexts/nbThreads)], allUrls))
        t.start()
        threads.append(t)

    # Wait for threads
    for thread in threads:
        thread.join()

    return allUrls


def deleteDoublonFromUrlList(urlList):
    cleanList = []
    for url in urlList:
       if url not in cleanList:
          cleanList.append(url)
    return cleanList

# test deleteDoublonFromUrlList
# print(getUrlsFromText("BRAD is the comprehensive online authority for essential advertising information on over 12,800 UK media titles. We've found BRAD to be a great data resource for us, which allows us to build highly targeted lists in an instant. They have been extremely helpful, from running comprehensive training sessions to dealing with last minute requests."))
# print(deleteDoublonFromUrlList(['http://dbpedia.org/resource/Brad_Pitt', 'http://dbpedia.org/resource/Comprehensive_school', 'http://dbpedia.org/resource/Authority', 'http://dbpedia.org/resource/Essentialism', 'http://dbpedia.org/resource/Advertising', 'http://dbpedia.org/resource/Title', 'http://dbpedia.org/resource/Brad_Pitt', 'http://dbpedia.org/resource/Data', 'http://dbpedia.org/resource/Resource', 'http://dbpedia.org/resource/Building', 'http://dbpedia.org/resource/Running', 'http://dbpedia.org/resource/Comprehensive_school', 'http://dbpedia.org/resource/Training']))

# TEST
# res = getUrlsFromText("""President Obama called Wednesday on Congress to extend a tax break
#    for students included in last year's economic stimulus package, arguing
#    that the policy provides more generous assistance.""")


if __name__ == '__main__':
    res = getUrlsFromTexts([{'text':"Berlin Germany beer Warsaw", 'url':'http://dbpedia.osef.org'}, {'url':'coucou', 'text':"""President Obama called Wednesday on Congress to extend a tax break
    for students included in last year's economic stimulus package, arguing
    that the policy provides more generous assistance."""}])
