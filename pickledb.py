#!/usr/bin/env python

# Copyright (c) 2011, Harrison Erd
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, 
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this 
# list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation 
# and/or other materials provided with the distribution.
# Neither the name of the Harrison Erd nor the names of its contributors 
# may be used to endorse or promote products derived from this software 
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "
# AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS 
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
# THE POSSIBILITY OF SUCH DAMAGE.

import pickle
# for json comment out the above line and uncomment the following line.
# import json as pickle

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

def llen(name):
    return len(db[name])

def append(key, more):
    tmp = db[key]
    db[key] = ('%s%s' % (tmp, more))
    pickle.dump(db, open(loco, 'wb'))
    return True

def lappend(name, pos, more):
    tmp = db[name][pos]
    db[name][pos] = ('%s%s' % (tmp, more))
    pickle.dump(db, open(loco, 'wb'))
    return True
