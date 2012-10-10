#!/usr/bin/python

import ez_setup
ez_setup.use_setuptools()
from setuptools import setup

setup(name='MusicCollectionOrganizer',
      version='0.1',
      description='''TODO''',
      author='Grzegorz Lachowski',
      author_email='grzgrzlac@gmail.com',
      url='https://launchpad.net/musiccollectionorganizer',
      requires=['mutagen', 'pylast', 'UnRAR2', 'lxml'],
      package_dir={'':'music_collection_organizer', 'tests':'tests'},
      packages=['file', 'music', '.'],
      test_suite='tests',
      scripts=['src/musicCollectionOrganizer']
     )
