import time
import os
import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from sklearn.preprocessing import MinMaxScaler


"""
[Decimal] acousticness:
Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.

[Decimal] danceability:
Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.

[Decimal] energy:
Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.

[Decimal] loudness:
The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db.

[Decimal] speechiness:
Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.

[Decimal] acousticness:
A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.

[Decimal] instrumentalness:
Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.

[Decimal] valence:
A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).

[Decimal] tempo:
The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.
"""
csv_file = "SpotifyAudioFeaturesNov2018.csv"


class FuzzyMusic(object):

    def __init__(self):
        self.df_2018 = pd.read_csv(csv_file)
        self.X = None

        self.userMood = None
        self.danceability = None
        self.valence = None
        self.userEnergy = None
        self.energy = None
        self.tempo = None
        self.userPref = None
        self.acousticness = None
        self.instrumentalness = None
        self.musicScore = None

        self.format_data()
        self.fuzzy_init()

    def format_data(self):
        self.X = self.df_2018.filter(items=['acousticness', 'danceability', 'energy', 'loudness', 'speechiness',
                                            'instrumentalness', 'valence', 'tempo', 'key', 'mode', 'time_signature',
                                            'popularity'])
        X_columns = self.X.columns

        # scale it to range of 0-10
        min_max_scaler = MinMaxScaler(feature_range=(0, 10))
        self.X = min_max_scaler.fit_transform(self.X)
        self.X = pd.DataFrame(self.X)
        self.X.columns = X_columns

        self.X['track_name'] = self.df_2018['track_name']
        self.X['track_id'] = self.df_2018['track_id']
        self.X['artist_name'] = self.df_2018['artist_name']

    def fuzzy_init(self):
        # Antecedent/Consequent objects, universe crisp value
        # user's mood
        self.userMood = ctrl.Antecedent(np.arange(0, 11, 1), 'userMood')
        self.danceability = ctrl.Antecedent(
            np.arange(0, 11, 1), 'danceability')
        self.valence = ctrl.Antecedent(np.arange(0, 11, 1), 'valence')
        # user's energy
        self.userEnergy = ctrl.Antecedent(np.arange(0, 11, 1), 'userEnergy')
        self.energy = ctrl.Antecedent(np.arange(0, 11, 1), 'energy')
        self.tempo = ctrl.Antecedent(np.arange(0, 11, 1), 'tempo')
        # user's preference
        self.userPref = ctrl.Antecedent(np.arange(0, 11, 1), 'userPref')
        self.acousticness = ctrl.Antecedent(
            np.arange(0, 11, 1), 'acousticness')
        self.instrumentalness = ctrl.Antecedent(
            np.arange(0, 11, 1), 'instrumentalness')

        # music_score 0-10
        self.musicScore = ctrl.Consequent(np.arange(0, 11, 1), 'musicScore')
        self.musicScore['very_poor'] = fuzz.trimf(
            self.musicScore.universe, [0, 2, 4])
        self.musicScore['poor'] = fuzz.trimf(
            self.musicScore.universe, [1, 3, 5])
        self.musicScore['average'] = fuzz.trimf(
            self.musicScore.universe, [3, 5, 7])
        self.musicScore['good'] = fuzz.trimf(
            self.musicScore.universe, [5, 7, 9])
        self.musicScore['very_good'] = fuzz.trimf(
            self.musicScore.universe, [6, 8, 10])

        # Not in use yet
        # loudness = ctrl.Antecedent(np.arange(0, 3, 1), 'loudness')
        # speechiness = ctrl.Antecedent(np.arange(0, 3, 1), 'speechiness')
        # user's mood
        self.userMood.automf(3)
        self.danceability.automf(3)
        self.valence.automf(3)
        # user's energy
        self.userEnergy.automf(3)
        self.energy.automf(3)
        self.tempo.automf(3)
        # user's preference
        self.userPref.automf(3)
        self.acousticness.automf(3)
        self.instrumentalness.automf(3)

        self.musicScore.view()

    def fuzzy_rules(self):
        try:
            # mood of music, relax, commute, exerise
            rules = []

            # user mood, danceability, valence
            rules.append(ctrl.Rule(self.userMood['poor'] & self.danceability['poor'] & self.valence['poor'],
                                   self.musicScore['good']))
            rules.append(ctrl.Rule(self.userMood['poor'] & self.danceability['poor'] | self.valence['poor'],
                                   self.musicScore['poor']))
            rules.append(ctrl.Rule(self.userMood['poor'] & self.danceability['good'] | self.valence['good'],
                                   self.musicScore['poor']))
            rules.append(ctrl.Rule(self.userMood['poor'] & self.danceability['average'] | self.valence['average'],
                                   self.musicScore['poor']))
            rules.append(ctrl.Rule(self.userMood['poor'] & self.danceability['good'] & self.valence['good'],
                                   self.musicScore['very_poor']))
            rules.append(ctrl.Rule(self.userMood['poor'] & self.danceability['average'] & self.valence['average'],
                                   self.musicScore['very_poor']))

            rules.append(ctrl.Rule(self.userMood['average'] & self.danceability['average'] & self.valence['average'],
                                   self.musicScore['good']))
            rules.append(ctrl.Rule(self.userMood['average'] & self.danceability['average'] | self.valence['average'],
                                   self.musicScore['poor']))
            rules.append(ctrl.Rule(self.userMood['average'] & self.danceability['good'] | self.valence['good'],
                                   self.musicScore['poor']))
            rules.append(ctrl.Rule(self.userMood['average'] & self.danceability['poor'] | self.valence['poor'],
                                   self.musicScore['poor']))
            rules.append(ctrl.Rule(self.userMood['average'] & self.danceability['good'] & self.valence['good'],
                                   self.musicScore['very_poor']))
            rules.append(ctrl.Rule(self.userMood['average'] & self.danceability['poor'] & self.valence['poor'],
                                   self.musicScore['very_poor']))

            rules.append(ctrl.Rule(self.userMood['good'] & self.danceability['good'] & self.valence['good'],
                                   self.musicScore['good']))
            rules.append(ctrl.Rule(self.userMood['good'] & self.danceability['good'] | self.valence['good'],
                                   self.musicScore['poor']))
            rules.append(ctrl.Rule(self.userMood['good'] & self.danceability['poor'] | self.valence['poor'],
                                   self.musicScore['poor']))
            rules.append(ctrl.Rule(self.userMood['good'] & self.danceability['average'] | self.valence['average'],
                                   self.musicScore['poor']))
            rules.append(ctrl.Rule(self.userMood['good'] & self.danceability['good'] & self.valence['good'],
                                   self.musicScore['very_poor']))
            rules.append(ctrl.Rule(self.userMood['good'] & self.danceability['average'] & self.valence['average'],
                                   self.musicScore['very_poor']))

            # user energy, energy, tempo
            rules.append(
                ctrl.Rule(self.userEnergy['poor'] & self.energy['poor'] & self.tempo['poor'],
                          self.musicScore['very_good']))
            rules.append(
                ctrl.Rule(self.userEnergy['poor'] & self.energy['poor'] | self.tempo['poor'],
                          self.musicScore['average']))
            rules.append(
                ctrl.Rule(self.userEnergy['poor'] & self.energy['good'] | self.tempo['good'], self.musicScore['poor']))
            rules.append(ctrl.Rule(self.userEnergy['poor'] & self.energy['average'] | self.tempo['average'],
                                   self.musicScore['poor']))
            rules.append(
                ctrl.Rule(self.userEnergy['poor'] & self.energy['good'] & self.tempo['good'],
                          self.musicScore['very_poor']))
            rules.append(ctrl.Rule(self.userEnergy['poor'] & self.energy['average'] & self.tempo['average'],
                                   self.musicScore['very_poor']))

            rules.append(ctrl.Rule(self.userEnergy['average'] & self.energy['average'] & self.tempo['average'],
                                   self.musicScore['very_good']))
            rules.append(ctrl.Rule(self.userEnergy['average'] & self.energy['average'] | self.tempo['average'],
                                   self.musicScore['average']))
            rules.append(
                ctrl.Rule(self.userEnergy['average'] & self.energy['good'] | self.tempo['good'],
                          self.musicScore['poor']))
            rules.append(
                ctrl.Rule(self.userEnergy['average'] & self.energy['poor'] | self.tempo['poor'],
                          self.musicScore['poor']))
            rules.append(ctrl.Rule(self.userEnergy['average'] & self.energy['poor'] & self.tempo['poor'],
                                   self.musicScore['very_poor']))
            rules.append(ctrl.Rule(self.userEnergy['average'] & self.energy['good'] & self.tempo['good'],
                                   self.musicScore['very_poor']))

            rules.append(
                ctrl.Rule(self.userEnergy['good'] & self.energy['good'] & self.tempo['good'],
                          self.musicScore['very_good']))
            rules.append(
                ctrl.Rule(self.userEnergy['good'] & self.energy['good'] | self.tempo['good'],
                          self.musicScore['average']))
            rules.append(
                ctrl.Rule(self.userEnergy['good'] & self.energy['poor'] | self.tempo['poor'], self.musicScore['poor']))
            rules.append(ctrl.Rule(self.userEnergy['good'] & self.energy['average'] | self.tempo['average'],
                                   self.musicScore['poor']))
            rules.append(
                ctrl.Rule(self.userEnergy['good'] & self.energy['poor'] & self.tempo['poor'],
                          self.musicScore['very_poor']))
            rules.append(ctrl.Rule(self.userEnergy['good'] & self.energy['average'] & self.tempo['average'],
                                   self.musicScore['very_poor']))

            # user preference, acousticness, instrumentalness
            rules.append(ctrl.Rule(self.userPref['poor'] & self.acousticness['poor'] & self.instrumentalness['poor'],
                                   self.musicScore['very_good']))
            rules.append(ctrl.Rule(self.userPref['poor'] & self.acousticness['poor'] | self.instrumentalness['poor'],
                                   self.musicScore['poor']))
            rules.append(ctrl.Rule(self.userPref['poor'] & self.acousticness['good'] | self.instrumentalness['good'],
                                   self.musicScore['poor']))
            rules.append(
                ctrl.Rule(self.userPref['poor'] & self.acousticness['average'] | self.instrumentalness['average'],
                          self.musicScore['poor']))
            rules.append(
                ctrl.Rule(self.userPref['poor'] & self.acousticness['average'] & self.instrumentalness['average'],
                          self.musicScore['very_poor']))
            rules.append(ctrl.Rule(self.userPref['poor'] & self.acousticness['good'] & self.instrumentalness['good'],
                                   self.musicScore['very_poor']))

            rules.append(
                ctrl.Rule(self.userPref['average'] & self.acousticness['average'] & self.instrumentalness['average'],
                          self.musicScore['very_good']))
            rules.append(
                ctrl.Rule(self.userPref['average'] & self.acousticness['average'] | self.instrumentalness['average'],
                          self.musicScore['average']))
            rules.append(ctrl.Rule(self.userPref['average'] & self.acousticness['poor'] | self.instrumentalness['poor'],
                                   self.musicScore['poor']))
            rules.append(ctrl.Rule(self.userPref['average'] & self.acousticness['good'] | self.instrumentalness['good'],
                                   self.musicScore['poor']))
            rules.append(ctrl.Rule(self.userPref['average'] & self.acousticness['poor'] & self.instrumentalness['poor'],
                                   self.musicScore['very_poor']))
            rules.append(ctrl.Rule(self.userPref['average'] & self.acousticness['good'] & self.instrumentalness['good'],
                                   self.musicScore['very_poor']))

            rules.append(ctrl.Rule(self.userPref['good'] & self.acousticness['good'] & self.instrumentalness['good'],
                                   self.musicScore['very_good']))
            rules.append(ctrl.Rule(self.userPref['good'] & self.acousticness['good'] | self.instrumentalness['good'],
                                   self.musicScore['average']))
            rules.append(ctrl.Rule(self.userPref['good'] & self.acousticness['poor'] | self.instrumentalness['poor'],
                                   self.musicScore['poor']))
            rules.append(ctrl.Rule(self.userPref['good'] & self.acousticness['good'] | self.instrumentalness['good'],
                                   self.musicScore['poor']))
            rules.append(ctrl.Rule(self.userPref['good'] & self.acousticness['poor'] & self.instrumentalness['poor'],
                                   self.musicScore['very_poor']))
            rules.append(
                ctrl.Rule(self.userPref['good'] & self.acousticness['average'] & self.instrumentalness['average'],
                          self.musicScore['very_poor']))

            music_score_ctrl = ctrl.ControlSystem(rules)
            music_score_sim = ctrl.ControlSystemSimulation(music_score_ctrl)
            return music_score_sim
        except Exception as e:
            print(str(e))

    def suggest_music(self, userInputs, n_samples=1000):
        """
        userInputs: [userMood, userEnergy, userPref]
        """

        music_score_sim = self.fuzzy_rules()
        music_score_sim.input['userMood'] = userInputs[0]
        music_score_sim.input['userEnergy'] = userInputs[1]
        music_score_sim.input['userPref'] = userInputs[2]

        sub_df = self.X.sample(n=n_samples, replace=False)
        print('suggesting music...')
        for idx, song in sub_df.iterrows():
            # userMood
            music_score_sim.input['danceability'] = song['danceability']
            music_score_sim.input['valence'] = song['valence']
            # userEnergy
            music_score_sim.input['energy'] = song['energy']
            music_score_sim.input['tempo'] = song['tempo']
            # userPref
            music_score_sim.input['acousticness'] = song['acousticness']
            music_score_sim.input['instrumentalness'] = song['instrumentalness']

            music_score_sim.compute()
            sub_df.at[idx, 'musicScore'] = round(
                music_score_sim.output['musicScore'], 3)
            # sub_df['musicScore'] = round(
            #     music_score_sim.output['musicScore'], 3)
            # print(song['danceability'], song['valence'], round(
            #     music_score_sim.output['musicScore'], 3))

        return sub_df
