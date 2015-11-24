# Web Semantique

# Moteur de recherche sémantique de cinéma
Services utilisés : dbpedia, alchemy

## Technos :
 - bash
 - python3 (Flask, SPARQLWrapper, requests)

## Pour lancer le serveur web:
`$ python3 server.py`

## Pour tester sans serveur web:
`$ python3 main.py`

## Clé google pour l'API Google Custom Search
Pour créer une nouvelle clé il faut :
 - Aller sur la [console google](https://console.developers.google.com)
 - Créer un nouveau projet
 - Activer l'API Google Custom Search pour ce projet
 - [Créer une clé](https://support.google.com/cloud/answer/6158862?hl=en&ref_topic=6262490) pour ce projet
 - C'est tout

**On est limité à 100 requêtes par jour par clé et 1 requête par secondes par utilisateur**