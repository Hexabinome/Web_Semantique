# -*- coding: utf-8 -*-

import re
from urllib.parse import quote
import json
import os
import random
from ast import literal_eval
import requests

CACHE_DIRECTORY_ALCHEMY = 'cache/alchemy'
CACHE_DIRECTORY_GOOGLE = 'cache/google'

# Note : on est limité à 100 requêtes par jour donc à utiliser avec parcimonie
# Le moteur de recherche est configuré pour privilégier les résultats qui sont liés au cinema
GOOGLE_API_KEY_1 = "AIzaSyB1Tqy8xyxFx7JqfsxNL2yyVrJdLxAMv14"  # Momo
GOOGLE_API_KEY_2 = "AIzaSyAu37WsyKygVkMwMJ8OFP4NMtP4j9Afys8"  # Momo
GOOGLE_API_KEY_3 = "AIzaSyAURhklAaMmv8UG0cLBAMdVJqbVDUbU_s0"  # Robin
GOOGLE_API_KEY_4 = "AIzaSyAcF9vr-X9VdKYau97nbN3PGsqeZrKqT7w"  # Momo

# Identifiant de notre moteur de recherche
CX = "002939247705119679953:0kfwzt0baty"
CX_TEST = "017576662512468239146:omuauf_lfve"

ALCHEMY_API_KEY = "691b05b66974d5e2c59a2d3d3fa950e7b98d5fcd"


def get_random_api_key():
    """
    Renvoie une clé au hasard parmi l'ensemble des clés à notre disposition
    :return:
    """
    liste_api = [GOOGLE_API_KEY_2, GOOGLE_API_KEY_3, GOOGLE_API_KEY_4]
    return random.choice(liste_api)


def google_search(searchInput, start_page):
    """
    Effectue une recherche sur google et renvoie les résultats sous forme de liens en json
    :param search_input: le texte à chercher
    :param start_page: index tu premier resultat
    :return: [{link : "http://..."},{link : "http://..."}]
    """
    cache_file = '{0}/{1}.{2}.google.txt'.format(CACHE_DIRECTORY_GOOGLE,
                                                 searchInput.replace('http://', '').replace('/', '_').replace(':',
                                                                                                              '_').replace(
                                                     '?', '_'),
                                                 start_page)

    if os.path.isfile(cache_file):
        resp = {}
        with open(cache_file, 'r') as f:
            try:
                resp = literal_eval(f.read())
                # print("Loaded {0} from cache".format(cache_file))
            except:
                pass
        # After loading, if didn't work or file was empty, delete cache and send request as usual
        if len(resp) == 0:
            os.remove(cache_file)
            print("Error loading from cache")
            return google_search(searchInput, start_page)
    else:
        searchInput = quote(searchInput)
        request_url = "https://www.googleapis.com/customsearch/v1"
        payload = {'key': get_random_api_key(), 'cx': CX, 'q': searchInput, 'start': start_page, 'item': 'items(link)'}
        response = requests.get(request_url, params=payload)
        assert response.status_code == 200
        resp = response.json()["items"]

        # Save in cache
        if not os.path.exists(CACHE_DIRECTORY_GOOGLE):
            os.makedirs(CACHE_DIRECTORY_GOOGLE)
        try:
            with open(cache_file, 'w') as f:
                f.write(str(resp))
                # print('Saved in cache (alchemy) {0}'.format(cache_file))
        except:
            # print('Cache writing error (alchemy) {0}'.format(cache_file))
            pass

    return resp


def alchemy_api(url):
    """
    Récupère le text brute de l'url passé en paramètre grâce à alchemy API
    :param url:
    :return: {"url" : "http://...", "text":"zeiruyzeiur"}
    """

    cache_file = '{0}/{1}.alchemy.txt'.format(CACHE_DIRECTORY_ALCHEMY,
                                              url.replace('http://', '').replace('/', '_').replace(':', '_').replace(
                                                  '?', '_'))
    # Load cache
    if os.path.isfile(cache_file):
        text = ''
        with open(cache_file, 'r', encoding='utf-8') as f:
            try:
                text = str(f.read())
                json_string = {'url': url, 'text': text}
                # print("Loaded {0} from cache".format(cache_file))
            except:
                pass
        # After loading, if didn't work or file was empty, delete cache and send request as usual
        if not text.strip():
            os.remove(cache_file)
            # print("Error loading from cache")
            return alchemy_api(url)
    # No cache existing
    else:
        request_url = "http://access.alchemyapi.com/calls/url/URLGetText"
        payload = {'apikey': ALCHEMY_API_KEY, 'url': url, 'outputMode': 'json'}
        response = requests.get(request_url, params=payload)

        assert response.status_code == 200
        text = response.json()["text"]
        # suppréssions de quelques caractères
        text = text.replace('\n', '')
        text = text.replace('\t', '')
        text = re.sub(' +', ' ', text)
        # Save in cache
        if not os.path.exists(CACHE_DIRECTORY_ALCHEMY):
            os.makedirs(CACHE_DIRECTORY_ALCHEMY)
        try:
            with open(cache_file, 'w') as f:
                f.write(str(text.encode('utf-8')))
                # print('Saved in cache (alchemy) {0}'.format(cache_file))
        except:
            # print('Cache writing error (alchemy) {0}'.format(cache_file))
            pass

    json_string = {"url": url, "text": text}
    return json_string


def do_module1_job(search_input, start_page=None):
    """
    Fais tout le taff du module 1 : prendre une requete, faire une recherche sur google, envoyer le texte contenu dans l'ensemble
    des pages renvoyées par google
    :param search_input:
    :param start_page:
    :return:
    """
    if start_page is None:
        start_page = 1

    result = []
    links = google_search(search_input, start_page)
    print("retour google : ", links)
    for link in links:
        result.append(alchemy_api(link["link"]))

    json_string = {"resultats": result}
    print("retour alchemy :", json_string)
    return json.dumps(json_string, ensure_ascii=False)


if __name__ == "__main__":
    print(do_module1_job("chuck norris"))
