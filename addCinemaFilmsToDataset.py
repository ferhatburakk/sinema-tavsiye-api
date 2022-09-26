import csv
import json
from urllib import response
from flask import jsonify
import requests

url = 'https://api.themoviedb.org/3/movie/now_playing'
searchResponse = requests.get(
    url, params={"api_key": "0bae694d311cd87f04fa14c8a7739a91", "region": "TR", "page":1})
json_response = searchResponse.json()

#print(json_response)


field_names = ['show_id', 'type', 'title', 'director', 'cast', 'country',
               'date_added', 'release_year', 'rating', 'duration', 'listed_in', 'description']
for key in json_response['results']:
    dict = {'show_id': key['id'],
            'type': 'Movie', 'title': 'vizyon' + key['title'],
            'director': '', 'cast': '', 'country': key['original_language'], 'date_added': key['release_date'],
            'release_year': key['release_date'], 'rating': key['vote_average'], 'duration': '', 'listed_in': 'Movies',
            'description': key['overview']
            }
    print(dict)
    with open('netflix_titles.csv', 'a') as f_object:

        dictwriter_object = csv.DictWriter(
            f_object, fieldnames=field_names)

        dictwriter_object.writerow(dict)

    f_object.close()   

