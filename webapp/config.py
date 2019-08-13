import types
import datetime
import os
import json
import calendar


basedir = os.path.dirname(os.path.realpath(__file__))

config_dict = {'db_host': '192.168.1.3',
               'db_port': 27017}


def get_value(key):
    """given key, return its value from the config dict"""
    try:
        return config_dict[key]
    except KeyError:
        return None


""" Environment Configuration """
def get_now():
    return calendar.timegm(datetime.datetime.now().timetuple())

def get_creds(path, crypt=False):
    path = os.path.join(basedir, path)
    if os.path.exists(path):
        with open(path, 'r') as fp: 
            j = json.load(fp)
        return j

