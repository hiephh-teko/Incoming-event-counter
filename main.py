# coding=utf-8
from datetime import datetime, timedelta
import logging
import os
from dotenv import load_dotenv
_DOT_ENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(_DOT_ENV_PATH)


def enter():
    print("############ START JOB ############")

from counter.counter import Counter 
Counter().enter()

