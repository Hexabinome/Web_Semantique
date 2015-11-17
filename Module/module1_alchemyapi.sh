#!/bin/bash
# Ce script récupère une URL et appel l'API Alchemy pour extraire le texte de la page.
# Usage : 02-alchemyapi.sh url
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
curl ${URLCURL} | ./jq-linux64 '. | {url : .url, text : .text}'

