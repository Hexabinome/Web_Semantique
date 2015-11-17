# ------------------------------------------
#           get_spotlight_uri
# ------------------------------------------
import requests, json


# TODO: making the confidence and support changeable
def getUrlFromText(jsonText):

    data = {'text' : jsonText,
        'confidence' : '0.2',
        'support' : '20' }

    url = 'http://spotlight.dbpedia.org/rest/annotate/'
    header = {'Accept' : 'application/json '}#, 'Content-Type' : 'application/json'}
    req = requests.post(url, data, headers=header)

    # TODO can throw error. Check status code 200
    jsonResponse = json.loads(req.text)

    urlList = []
    for resource in jsonResponse[u'Resources']:
        urlList.append(resource[u'@URI'])
    return urlList

# TEST
print(getUrlFromText("""President Obama called Wednesday on Congress to extend a tax break
    for students included in last year's economic stimulus package, arguing
    that the policy provides more generous assistance."""))
