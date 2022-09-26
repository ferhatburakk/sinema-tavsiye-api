# Önerilen şarkıcıların konserlerinin olup olmadığının kontrolü
import json
from urllib import response
from flask import jsonify
import requests
import csv


def addFilm(title):

    url = 'https://api.themoviedb.org/3/search/movie'
    searchResponse = requests.get(
        url, params={"api_key": "0bae694d311cd87f04fa14c8a7739a91", "query": title})
    json_response = searchResponse.json()

    field_names = ['show_id', 'type', 'title', 'director', 'cast', 'country',
                   'date_added', 'release_year', 'rating', 'duration', 'listed_in', 'description']

    for key in json_response['results']:
        dict = {'show_id': key['id'],
                'type': 'Movie', 'title': key['title'],
                'director': '', 'cast': '', 'country': key['original_language'], 'date_added': key['release_date'],
                'release_year': '', 'rating': key['vote_average'], 'duration': '', 'listed_in': 'Movies',
                'description': key['overview']
                }
        print(len(json_response['results']))
        print(json_response['results'])
        with open('netflix_titles.csv', 'a', encoding='utf-8-sig') as f_object:

            dictwriter_object = csv.DictWriter(
                f_object, fieldnames=field_names)

            dictwriter_object.writerow(dict)

            f_object.close()

addFilm("Jurassic World")