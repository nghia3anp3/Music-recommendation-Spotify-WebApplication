# PUT ALL YOUR NON-FUNCTION CODE OVER HERE
# EGS: IMPORT STATEMENTS, LOADING PICKLE FILES / MODELS, DATASET/JSON PROCESSING, ETC.

# REMEMBER TO PLACE YOUR FILES (.PICKLE ETC.) IN THE FOLDER ABOVE THIS ONE I.E.
# IN THE SAME FOLDER AS RUN_APP.PY


# THIS IS YOUR MAIN FUNCTION!
def recommend_similar_songs(audio_features, lyrics_features):
    # PUT YOUR FUNCTION CODE HERE!
    return final_result_dictionary

# THIS FUNCTION CONVERTS THE AUDIO FEATURES INTO A LIST BEFORE SENDING THEM TO
# recommend_similar_songs
def get_similar_songs(features, lyrics):
  print(features)
  print(lyrics)

  # features is a dict. convert it to a list using the same order as the assignments...
  audio_feature_headers = ['key', 'energy', 'liveness', 'tempo', 'speechiness', 'acousticness', 'instrumentalness', 'time_signature', 'duration', 'loudness', 'valence', 'danceability', 'mode', 'time_signature_confidence', 'tempo_confidence', 'key_confidence', 'mode_confidence']
  audio_features_list = []

  for audio_feature_name in audio_feature_headers:
      audio_features_list.append(features[audio_feature_name])

  # Provide the lyrics as is; a string

  return recommend_similar_songs(audio_features_list, lyrics)
