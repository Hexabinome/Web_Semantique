import requests
import re
from urllib.parse import quote
import json
import os
import pprint

CACHE_DIRECTORY = 'cache'

# Note : on est limité à 100 requêtes par jour donc à utiliser avec parcimonie
# Le moteur de recherche est configuré pour privilégier les résultats qui sont liés au cinema
GOOGLE_API_KEY_1 = "AIzaSyB1Tqy8xyxFx7JqfsxNL2yyVrJdLxAMv14"
GOOGLE_API_KEY_2 = "AIzaSyDnspc_W9FF5TIWfpNXc8kENjRVdp-GpW0"
GOOGLE_API_KEY_3 = "AIzaSyAURhklAaMmv8UG0cLBAMdVJqbVDUbU_s0"
# Identifiant de notre moteur de recherche
CX = "002939247705119679953:0kfwzt0baty"
CX_TEST = "017576662512468239146:omuauf_lfve"

ALCHEMY_API_KEY = "691b05b66974d5e2c59a2d3d3fa950e7b98d5fcd"


def google_search(search_input, start_page):
    """
    Effectue une recherche sur google et renvoie les résultats sous forme de liens en json
    :param search_input: le texte à chercher
    :param start_page: index tu premier resultat
    :return: [{link : "http://..."},{link : "http://..."}]
    """
    search_input = quote(search_input)
    request_url = "https://www.googleapis.com/customsearch/v1"
    payload = {'key': GOOGLE_API_KEY_2, 'cx': CX, 'q': search_input, 'start': start_page, 'item': 'items(link)'}
    response = requests.get(request_url, params=payload)
    assert response.status_code == 200
    # pprint(respone.json()["items"])
    return response.json()["items"]


def alchemy_api(url):
    """
    Récupère le text brute de l'url passé en paramètre grâce à alchemy API
    :param url:
    :return: {"url" : "http://...", "text":"zeiruyzeiur"}
    """

    cache_file = '{0}/{1}.alchemy.txt'.format(CACHE_DIRECTORY,
                                              url.replace('http://', '').replace('/', '_').replace(':', '_'))
    # Load cache
    if os.path.isfile(cache_file):
        text = ''
        with open(cache_file, 'r') as f:
            try:
                text = f.read()
                json_string = {'url': url, 'text': text}
                # print("Loaded {0} from cache".format(cache_file))
            except:
                pass
        # After loading, if didn't work or file was empty, delete cache and send request as usual
        if not text.strip():
            os.remove(cache_file)
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
        if not os.path.exists(CACHE_DIRECTORY):
            os.makedirs(CACHE_DIRECTORY)
        try:
            with open(cache_file, 'w') as f:
                f.write(text)
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
    for link in links:
        result.append(alchemy_api(link["link"]))

    json_string = {"resultats": result}
    return json.dumps(json_string, ensure_ascii=False)


if __name__ == "__main__":
    print(do_module1_job("dexter"))
