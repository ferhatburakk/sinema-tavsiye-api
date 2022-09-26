import csv
import json
from urllib import response
from flask import jsonify
import requests
import firebase_admin
from firebase_admin import credentials, firestore

url = 'https://api.themoviedb.org/3/movie/now_playing'
searchResponse = requests.get(url, params={
                              "api_key": "0bae694d311cd87f04fa14c8a7739a91", "region": "TR", "page": 1})
json_response = searchResponse.json()
total_pages = json_response['total_pages']
dbinfo = credentials.Certificate("firebase_info.json")

firebase_admin.initialize_app(dbinfo)

firestoreDb = firestore.client()
'''
field_names = ['show_id', 'type', 'title', 'director', 'cast', 'country',
               'date_added', 'release_year', 'rating', 'duration', 'listed_in', 'description']
for key in json_response['results']:
    dict = {'show_id': key['id'],
            'type': 'Movie', 'title': 'vizyon' + key['title'],
            'director': '', 'cast': '', 'country': key['original_language'], 'date_added': key['release_date'],
            'release_year': key['release_date'], 'rating': key['vote_average'], 'duration': '', 'listed_in': 'Movies',
            'description': key['overview']
            }
'''


def controlFilms(recommendedfilms):

    i = 1
    url = 'https://api.themoviedb.org/3/movie/now_playing'
    searchResponse = requests.get(url, params={
        "api_key": "0bae694d311cd87f04fa14c8a7739a91", "region": "TR", "page": i})

    json_response = searchResponse.json()
    total_pages = json_response['total_pages']
    # print(recommendedfilms)
    recommendedCinemaFilms = []
    while i <= total_pages:

        if recommendedfilms == 'not found':
            return
        for key1 in recommendedfilms['result']:
            filmName = key1['title']
            if filmName.startswith('vizyon'):
                key1['title'] = key1['title'].replace("vizyon", "")
        
        for key2 in json_response['results']:
            for key1 in recommendedfilms['result']:
                    if key2['original_title'] == key1['title']:
                        recommendedCinemaFilms.append(key2)
        i += 1
        searchResponse = requests.get(url, params={
            "api_key": "0bae694d311cd87f04fa14c8a7739a91", "region": "TR", "page": i})
        json_response = searchResponse.json()
    # print(recommendedCinemaFilms)
    return recommendedCinemaFilms


def addRecommendedCinemaFilmsToDatabase(filmsList, uid):

    print("databse metodu")
    print(filmsList)
    if filmsList is None:
        return
    datas = filmsList
    for key in datas:
        title = key['original_title']
        vote_average = key['vote_average']
        overview = key['overview']
        firestoreDb.collection(u'user_cinemas').add(
            {'uid': uid, 'film_name': title, 'overview': overview, 'vote': vote_average})
