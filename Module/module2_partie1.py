# ------------------------------------------
#           get_spotlight_uri
# ------------------------------------------
import urllib2, urllib, json


# TODO: making the confidence and support changeable
def getUrlFromText (jsonText):

  data = urllib.urlencode({'text' : jsonText,
   'confidence' : '0.2',
   'support' : '20' })

  url = 'http://spotlight.dbpedia.org/rest/annotate/'
  req = urllib2.Request(url, data, {'Accept' : 'application/json ', 'Content-Type' : 'application/json'})
  webResponse = urllib2.urlopen(req)

  jsonResponse = json.loads(webResponse.read())

  urlList = []
  for resource in jsonResponse[u'Resources']:
      urlList.append(resource[u'@URI'])
  return urlList


# TEST
# print getUrlFromText("""President Obama called Wednesday on Congress to extend a tax break
#    for students included in last year's economic stimulus package, arguing
#    that the policy provides more generous assistance.""")

