#! /bin/bash
# [Maxou]

#get sources of search result page
PAGE_SOURCE=$(curl -s -A 'Mozilla/5.0 (X11; Linux i686; rv:5.0) Gecko/20100101 Firefox/5.0' "http://www.google.de/search?q=sunset+rubdown")

#extract all XYZ-urls from <a href="/url?q=XYZ> search results
echo $PAGE_SOURCE | sed 's/>/>\n/g' | grep -A1 "<h3" | sed 's/http/\nhttp/g' | grep http | sed 's/\">//g' > /tmp/linkfile




#extract target urls of search result page
#echo $PAGE_SOURCE | sed 's/>/>\n/g' | grep -A1 "<cite" | grep '<b>\|</cite>' | sed 's/<b>//g' | sed 's/<\/cite>//g'



