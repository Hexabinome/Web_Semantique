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

# filter all adds. Luckily all add urls are marked in the page sources. Their links begin with: "/aclk?sa="
# So I will filter all html elements containing this string.
FILTERED_SOURCE=$(echo $PAGE_SOURCE | sed 's/>/>\n/g' | grep --invert-match 'href="/aclk?sa=')

# extract all result-urls from result pages's html sources 
# the url container has the form <a href="/url?q=XYZ> 
RAW_LINKS=$(echo $FILTERED_SOURCE | sed 's/>/>\n/g' | grep -A1 "<h3" | sed 's/http/\nhttp/g' | sed 's/\&amp/\n/g' | grep http | sed 's/">//g')

# still the urls need to be refined, see table below for substitution rules
# more info: https://en.wikipedia.org/wiki/Percent-encoding
# %21 -> !
# %23 -> #
# %24 -> $
# %26 -> &
# %27 -> '
# %28 -> (
# %29 -> )
# %2A -> *
# %2B -> +
# %2C -> ,
# %2F -> /
# %3A -> :
# %3B -> ;
# %3D -> =
# %3F -> ?
# %40 -> @
# %5B -> [
# %5D -> ]
echo $RAW_LINKS | sed 's/ /\n/g' \
		| sed 's/%21/!/g' \
	       | sed 's/%23/#/g' \
	       | sed 's/%24/$/g' \
	       | sed 's/%26/&/g' \
       	       | sed "s/%27/'/g" \
	       | sed 's/%28/(/g' \
	       | sed 's/%29/)/g' \
	       | sed 's/%2A/*/g' \
	       | sed 's/%2B/+/g' \
	       | sed 's/%2C/,/g' \
	       | sed 's/%2F/\//g' \
	       | sed 's/%3A/:/g' \
	       | sed 's/%3B/;/g' \
	       | sed 's/%3D/=/g' \
	       | sed 's/%3F/?/g' \
	       | sed 's/%40/@/g' \
	       | sed 's/%5B/[/g' \
	       | sed 's/%5D/]/g'

