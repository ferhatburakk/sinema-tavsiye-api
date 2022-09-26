from flask import Flask, request, jsonify
from recommendation_engine import recommended_shows  # Importing engine function
import pandas as pd
import pickle
from addFilmToDataset import addFilm
from controlFilms import controlFilms
from controlFilms import addRecommendedCinemaFilmsToDatabase

app = Flask(__name__)

# Avoid switching the order of 'title' and 'confidence' keys
app.config['JSON_SORT_KEYS'] = False

netflix_titles_df = pd.read_csv('netflix_titles.csv', usecols=[2])

tfidf_vect_pkl = pickle.load(open('tfidf_vectorizer.pickle', 'rb'))


@app.route('/getFilmRecommendation', methods=['GET'])
def process_request():

    args = request.args
    filmName = args['filmName']
    uid = args['uid']
    # Parse received JSON request

    # Extract show title
    title = filmName

    # Call recommendation engine
    recommended_shows_dict = recommended_shows(
        title, netflix_titles_df, tfidf_vect_pkl)

    if recommended_shows_dict == 'not found':
        addFilm(title)
        #recommendedCinemaFilms = controlFilms(recommended_shows_dict)
        #addRecommendedCinemaFilmsToDatabase(recommendedCinemaFilms, uid)
        # print('-----------------------')
    recommendedCinemaFilms = controlFilms(recommended_shows_dict)
    addRecommendedCinemaFilmsToDatabase(recommendedCinemaFilms, uid)
    print('-----------------------')
    return jsonify(recommended_shows_dict)


if __name__ == '__main__':
    app.run(debug=True)
