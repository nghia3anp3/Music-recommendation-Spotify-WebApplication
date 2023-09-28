# PUT ALL YOUR NON-FUNCTION CODE OVER HERE
# EGS: IMPORT STATEMENTS, LOADING PICKLE FILES / MODELS, DATASET/JSON PROCESSING, ETC.

# REMEMBER TO PLACE YOUR FILES (.PICKLE ETC.) IN THE FOLDER ABOVE THIS ONE I.E.
# IN THE SAME FOLDER AS RUN_APP.PY
import pandas as pd
import numpy as np
import pickle
from sklearn.datasets import load_diabetes
from string import punctuation
from nltk.stem.snowball import SnowballStemmer
from collections import namedtuple
import pprint   
import warnings

warnings.filterwarnings("ignore")
pp = pprint.PrettyPrinter(indent=4)
Song = namedtuple("Song", ["artist", "title"])
stemmer = SnowballStemmer('english')
df = pd.read_json("MasterSongList.json")

def fix(string):
    translator = str.maketrans('','',punctuation)
    string = "".join(string[0])
    stopwords = ['153','ContributorsTranslationsDeutschOne','Chorus','Verse 1','Verse 2','Brigde','Pre-Chorus','Outro','\n','lyrics']
    for word in stopwords:
        if word in string:
            string=string.replace(word," ")
    string = string.translate(translator)
    string = string.replace('    ',' ')
    string = string.replace('   ',' ')
    for x in string:
        x = stemmer.stem(x)
    string = " ".join(string.split(" ")[5:-1])
    return string.lower()

def is_in(li,list_moods):
    for x in li:
        if x in list_moods:
            return li
    return np.nan

def get_similar_song(list_moods, genres):
    temp_df = df
    temp_df['genres'] = temp_df['genres'].apply(lambda x: "".join(x))
    temp_df = temp_df[temp_df['genres']==genres]
    temp_df['moods'] = temp_df['moods'].apply(lambda x: is_in(x,list_moods))
    return temp_df

# THIS IS YOUR MAIN FUNCTION!
def recommend_similar_songs(audio_features, lyrics_features):
    lyric_model = pickle.load(open('model_lyrics.pkl', 'rb'))
    tfidf_vec = pickle.load(open('tfidf_vec.pkl','rb'))
    tfidf = pickle.load(open('tfidf.pkl','rb'))
    mlb = pickle.load(open('mlb.pkl','rb'))
    pickled_model = pickle.load(open('model.pkl', 'rb'))

    data = np.array(audio_features).reshape(1,-1)
    genres = pickled_model.predict(data)[0]
    list_moods = [mlb.inverse_transform(lyric_model.predict(tfidf_vec.transform([lyrics_features])))[0][0]]

    final_df = get_similar_song(list_moods, genres)
    final_df['genres'] = final_df['genres'].apply(lambda x: ''.join(x))
    result = final_df[~final_df['moods'].isna()][['artist','name']]
    dic = []
    for i in range(0,result.shape[0]):
        dic.append(result.iloc[i].to_list())
    res_dic = []
    for j in range(0, 10):
        for i in dic:
            res_dic.append(Song(artist=i[0], title=i[1]))
    
    final_result_dictionary = dict(playlist=res_dic)       
    final_result_dictionary['genre'] = genres
    final_result_dictionary['moods'] = list_moods
    final_result_dictionary['playlist'] = final_result_dictionary['playlist'][0:10]

    return final_result_dictionary

# THIS FUNCTION CONVERTS THE AUDIO FEATURES INTO A LIST BEFORE SENDING THEM TO
# recommend_similar_songs
def get_similar_songs(features, lyrics):
#   print(features)
#   print(lyrics)

  # features is a dict. convert it to a list using the same order as the assignments...
  audio_feature_headers = ['key', 'energy', 'liveness', 'tempo', 'speechiness', 'acousticness', 'instrumentalness', 'time_signature', 'duration', 'loudness', 'valence', 'danceability', 'mode', 'time_signature_confidence', 'tempo_confidence', 'key_confidence', 'mode_confidence']
  audio_features_list = []

  for audio_feature_name in audio_feature_headers:
      audio_features_list.append(features[audio_feature_name])

  # Provide the lyrics as is; a string
  lyrisc = fix(lyrics)
  return recommend_similar_songs(audio_features_list, lyrics)
