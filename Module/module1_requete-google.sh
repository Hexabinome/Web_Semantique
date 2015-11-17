#! /bin/bash
# [Maxou]

function usage()
{
    echo "No search term specified :("
    exit -1
}

if [ $# = 0 ]; then
    usage
fi

SUBJECT=$(echo $1 | sed 's/ /+/g')

# get sources of first google search result page
# I needed to change the user client because google blocks wget/curl requests
PAGE_SOURCE=$(curl -s -A 'Mozilla/5.0 (X11; Linux i686; rv:5.0) Gecko/20100101 Firefox/5.0' "http://www.google.co.uk/search?q=$SUBJECT")
#PAGE_SOURCE=$(curl -s -A 'Mozilla/5.0 (X11; Linux i686; rv:5.0) Gecko/20100101 Firefox/5.0' "http://www.google.de/search?q=$SUBJECT")

#echo $PAGE_SOURCE


# extract all result-urls from result pages's html sources 
# the container has the form <a href="/url?q=XYZ> 
echo $PAGE_SOURCE | sed 's/>/>\n/g' | grep -A1 "<h3" | sed 's/http/\nhttp/g' | sed 's/\&amp/\n/g' | grep http | sed 's/%3F/?/g' | sed 's/%3D/=/g' | sed 's/%2B/+/g'


