#!/usr/bin/env python


import sys
import pymongo
import traceback

import config


# set up the database stuff
from pymongo.monitoring import ServerHeartbeatListener

class HeartbeatFailedListener(ServerHeartbeatListener):
    def started(self, event):
        pass

    def succeeded(self, event):
        pass

    def failed(self, event):
        print('Heartbeat failed with exception: ', event.reply)

heartbeat_listener = HeartbeatFailedListener()
# conn = MongoClient('127.0.0.1', 27017, username='admin', password='admin',
#                    serverSelectionTimeoutMS=1000, event_listeners=[heartbeat_listener])

def build_conn(collection, host=config.get_value('db_host'), port=config.get_value('db_port')):
    try:
        client = pymongo.MongoClient('mongodb://{}:{}/'.format(host, port),
                    serverSelectionTimeoutMS=1000,
                    event_listeners=[heartbeat_listener])
        this_db = client.whereis
        coll_store = None
        if client:
            print('connected to mongodb')
        if collection == 'users':
            coll_store = this_db.users
        return coll_store
    except:
        traceback.print_exc(sys.exc_info())
        print('not connected to mongodb')

