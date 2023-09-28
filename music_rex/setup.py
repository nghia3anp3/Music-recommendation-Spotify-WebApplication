#!/usr/bin/env python

from setuptools import setup

setup(name='Music Rex',
      version='0.1',
      description='Music Rec',
      packages=['music_rex'],
      install_requires=[
            'flask',
            'spotipy',
            'lyricsgenius'
      ]
     )