# ------------------------------------------
#           get_spotlight_uri
# ------------------------------------------
import urllib2, urllib, json

def getUrlFromText (jsonText):
  # The data will be what is return by the previsous step
  data = urllib.urlencode({'text' : jsonText,
   'confidence' : '0.2',
   'support' : '20' })

  url = 'http://spotlight.dbpedia.org/rest/annotate/'
  req = urllib2.Request(url, data, {'Accept' : 'application/json ', 'Content-Type' : 'application/json'})
  f = urllib2.urlopen(req)

  resp = json.loads(f.read())

  urlList = []
  for x in resp[u'Resources']:
      urlList.append(x[u'@URI'])
  # print urlList
  return urlList


# TEST
# print getUrlFromText("""President Obama called Wednesday on Congress to extend a tax break
#    for students included in last year's economic stimulus package, arguing
#    that the policy provides more generous assistance.""")

