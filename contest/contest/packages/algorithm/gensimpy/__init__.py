"""
@TODO: there is a collision at gensimhttpapi folder. At this folder we have the same sources
"""

from gensim import similarities     
from gensim import utils
import sqlite3
import sqlitedict

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
