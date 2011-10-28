#!/usr/bin/env python

import pickle

def load(location):
    global db
    try:
        db = pickle.load(open(location, 'rb'))
    except IOError:
        db = {}
    global loco
    loco = location
    return True

def set(key, value):
    db[key] = value
    pickle.dump(db, open(loco, 'wb'))
    return True

def get(key):
    return db[key]

def rem(key):
    del db[key]
    pickle.dump(db, open(loco, 'wb'))
    return True

def lcreate(name):
    db[name] = []
    pickle.dump(db, open(loco, 'wb'))
    return True

def ladd(name, value):
    db[name].append(value)
    pickle.dump(db, open(loco, 'wb'))
    return True

def lgetall(name):
    return db[name]

def lget(name, pos):
    return db[name][pos]

def lrem(name):
    del db[name]
    pickle.dump(db, open(loco, 'wb'))
    return True

def lpop(name, pos):
    del db[name][pos]
    pickle.dump(db, open(loco, 'wb'))
    return True
