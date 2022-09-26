import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

netflix_titles_df = pd.read_csv('netflix_titles.csv')

netflix_titles_df.drop(
    netflix_titles_df.columns[[0, 1, 5, 6, 7, 9]], axis=1, inplace=True)

netflix_titles_df.fillna('', inplace=True)

netflix_titles_df[['director', 'cast']] = netflix_titles_df[[
    'director', 'cast']].applymap(lambda x: ' '.join(x.replace(' ', '').split(',')[:3]))

netflix_titles_df['title_dup'] = netflix_titles_df['title']

titles_corpus = netflix_titles_df.apply(' '.join, axis=1)

tfidf_vectorizer_params = TfidfVectorizer(
    lowercase=True, stop_words='english', ngram_range=(1, 3), max_df=.5)

tfidf_vectorizer = tfidf_vectorizer_params.fit_transform(titles_corpus)

pickle.dump(tfidf_vectorizer, open('tfidf_vectorizer.pickle', 'wb'))


def recommended_shows(title, shows_df, tfidf_vect):
    '''
    Recommends the top 5 similar shows to provided show title.
            Arguments:
                    title (str): Show title extracted from JSON API request
                    shows_df (pandas.DataFrame): Dataframe of Netflix shows dataset
                    tfidf_vect (scipy.sparse.matrix): sklearn TF-IDF vectorizer sparse matrix
            Returns:
                    response (dict): Recommended shows and similarity confidence in JSON format
    '''

    try:

        title_iloc = shows_df.index[shows_df['title'] == title][0]

    except:

        return 'not found'

    show_cos_sim = cosine_similarity(
        tfidf_vect[title_iloc], tfidf_vect).flatten()

    sim_titles_vects = sorted(
        list(enumerate(show_cos_sim)), key=lambda x: x[1], reverse=True)[1:80]

    response = {'result': [{'title': shows_df.iloc[t_vect[0]][0], 'confidence': round(
        t_vect[1], 1)} for t_vect in sim_titles_vects]}

    return response
