#!/bin/bash
# Ce script récupère une URL et appel l'API Alchemy pour extraire le texte de la page.
# Usage : module1_alchemy.sh url
#  => {url : url
#  	   text : textdelapage}

# Clé de l'api
APIKEY="691b05b66974d5e2c59a2d3d3fa950e7b98d5fcd"

# Mode de sortie
OUTPUTMODE="json"

# Url donné en entrée
URL=$1

# URL appelé par curl
URLCURL="http://access.alchemyapi.com/calls/url/URLGetText?apikey=${APIKEY}&url=${URL}&outputMode=${OUTPUTMODE}"

# Requete curl
curl -s ${URLCURL} |sed -e 's/\\n//g' -e 's/\\t//g' |tr -s " "| jq '. | {url : .url, text : .text}'

