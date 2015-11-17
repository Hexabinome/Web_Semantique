import urllib2, urllib

def getUrlFromText (text):
  # The data will be what is return by the previsous step
  data = urllib.urlencode({'text' : """President Obama called Wednesday on Congress to extend a tax break
   for students included in last year's economic stimulus package, arguing
   that the policy provides more generous assistance.""",
   'confidence' : '0.2',
   'support' : '20' })

  url = 'http://spotlight.dbpedia.org/rest/annotate/'
  req = urllib2.Request(url, data, {'Accept' : 'application/json '  }) #, 'Content-Type' : 'application/json'})
  f = urllib2.urlopen(req)

  ## DEBUG
  # for x in f:
  #     print(x)
  # f.close()
  ## end DEBUG
  return f
