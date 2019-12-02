import logging
from os.path import join, dirname
from dotenv import load_dotenv
import os


_logger = logging.getLogger(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__)
))


class ElasticsearchConfig(object):

    ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST')
    ELASTICSEARCH_PORT = os.getenv('ELASTICSEARCH_PORT')
    ELASTICSEARCH_HOURS_QUERY = os.getenv('ELASTICSEARCH_HOURS_QUERY')
    ELASTICSEARCH_SCROLL_SIZE = os.getenv('ELASTICSEARCH_SCROLL_SIZE')
    ELASTICSEARCH_SCROLL_TIME = os.getenv('ELASTICSEARCH_SCROLL_TIME')

print("init")
global counter 
counter = 0