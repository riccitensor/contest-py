#!/usr/bin/env python

from distutils.core import setup

setup(name='contest',
      version='0.2.0',
      description="""Some Projects in once. 
      1. A Plista Prize reference implemenation. 
      2. A Rest Api for the gensim Text Similarity Project
      3. A Cassandra Test Environment""",
      author='Christian Winkelmann',
      author_email='christian.winkelmann@plista.com',
      url='www.plista.com',
      packages=['contest',
                'contest.config',
                'contest.management',
                'contest.migrations',
                'contest.packages', 
                'contest.packages.algorithm',
                'contest.packages.algorithm.gensimpy',
                'contest.packages.algorithm.milk',
                'contest.packages.algorithm.tree_classifier', 
                'contest.packages.controller',
                'contest.packages.crawler',
                'contest.packages.designPatterns',
                'contest.packages.ensemble_mixing',
                'contest.packages.helper',
                'contest.packages.message_parsers', 
                'contest.packages.models',
                'contest.packages.models.test',
                'contest.packages.queues',
                'contest.packages.rabbitMQ',
                'contest.packages.rabbitMQ.algorithm',
                'contest.packages.rabbitMQ.algorithm.storage',
                'contest.packages.rabbitMQ.algorithm.recommender',
                'contest.packages.rabbitMQ.config',
                'contest.packages.rabbitMQ.test',
                'contest.packages.recommenders', 
                'contest.packages.statistics', 
                'contest.packages.queues',
                'contest.unitTests',
                'contest.unitTests.contestReplay',
                'contest.unitTests.impressionGenerator',
                'contest.unitTests.statistics',
                'contest.unitTests.syntheticTest',
                'contest.unitTests.test',
                'contest.unitTests.test.counters',
                'contest.unitTests.test.gensim',
                'contest.unitTests.riak_games',
                'contest.unitTests.test.testImport',                
                 ], requires=['redis'],
     )