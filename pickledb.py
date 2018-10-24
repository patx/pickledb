#!/usr/bin/env python3

# Copyright (c) 2018, Harrison Erd
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
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
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import sys
import os
import signal
import simplejson
from threading import Thread


def load(location, option):
    '''Return a pickledb object. location is the path to the json file.'''
    return pickledb(location, option)


class pickledb(object):

    key_string_error = TypeError('Key/name must be a string!')

    def __init__(self, location, option):
        '''Creates a database object and loads the data from the location path.
        If the file does not exist it will be created on the first update.'''
        self.load(location, option)
        self.dthread = None
        self.set_sigterm_handler()

    def __getitem__(self, item):
        '''Syntax sugar for get()'''
        return self.get(item)

    def __setitem__(self, key, value):
        '''Sytax sugar for set()'''
        return self.set(key, value)

    def __delitem__(self, key):
        '''Sytax sugar for rem()'''
        return self.rem(key)

    def set_sigterm_handler(self):
        '''Assigns sigterm_handler for graceful shutdown during dump()'''
        def sigterm_handler():
            if self.dthread is not None:
                self.dthread.join()
            sys.exit(0)
        signal.signal(signal.SIGTERM, sigterm_handler)

    def load(self, location, option):
        '''Loads, reloads or changes the path to the db file'''
        location = os.path.expanduser(location)
        self.loco = location
        self.fsave = option
        if os.path.exists(location):
            self._loaddb()
        else:
            self.db = {}
        return True

    def dump(self):
        '''Force dump memory db to file'''
        self._dumpdb(True)
        return True

    def set(self, key, value):
        '''Set the str value of a key'''
        if isinstance(key, str):
            self.db[key] = value
            self._dumpdb(self.fsave)
            return True
        else:
            raise self.key_string_error

    def get(self, key):
        '''Get the value of a key'''
        try:
            return self.db[key]
        except KeyError:
            return False

    def getall(self):
        '''Return a list of all keys in db'''
        return self.db.keys()

    def exists(self, key):
        '''Return True if key exists in db, return False if not'''
        return key in self.db

    def rem(self, key):
        '''Delete a key'''
        del self.db[key]
        self._dumpdb(self.fsave)
        return True

    def totalkeys(self, name=None):
        '''Get a total number of keys, lists, and dicts inside the db'''
        if name is None:
            total = len(self.db)
            return total
        else:
            total = len(self.db[name])
            return total

    def lcreate(self, name):
        '''Create a list, name must be str'''
        if isinstance(name, str):
            self.db[name] = []
            self._dumpdb(self.fsave)
            return True
        else:
            raise self.key_string_error

    def ladd(self, name, value):
        '''Add a value to a list'''
        self.db[name].append(value)
        self._dumpdb(self.fsave)
        return True

    def lextend(self, name, seq):
        '''Extend a list with a sequence'''
        self.db[name].extend(seq)
        self._dumpdb(self.fsave)
        return True

    def lgetall(self, name):
        '''Return all values in a list'''
        return self.db[name]

    def lget(self, name, pos):
        '''Return one value in a list'''
        return self.db[name][pos]

    def lrem(self, name):
        '''Remove a list and all of its values'''
        number = len(self.db[name])
        del self.db[name]
        self._dumpdb(self.fsave)
        return number

    def lpop(self, name, pos):
        '''Remove one value in a list'''
        value = self.db[name][pos]
        del self.db[name][pos]
        self._dumpdb(self.fsave)
        return value

    def llen(self, name):
        '''Returns the length of the list'''
        return len(self.db[name])

    def append(self, key, more):
        '''Add more to a key's value'''
        tmp = self.db[key]
        self.db[key] = tmp + more
        self._dumpdb(self.fsave)
        return True

    def lappend(self, name, pos, more):
        '''Add more to a value in a list'''
        tmp = self.db[name][pos]
        self.db[name][pos] = tmp + more
        self._dumpdb(self.fsave)
        return True

    def dcreate(self, name):
        '''Create a dict, name must be str'''
        if isinstance(name, str):
            self.db[name] = {}
            self._dumpdb(self.fsave)
            return True
        else:
            raise self.key_string_error

    def dadd(self, name, pair):
        '''Add a key-value pair to a dict, "pair" is a tuple'''
        self.db[name][pair[0]] = pair[1]
        self._dumpdb(self.fsave)
        return True

    def dget(self, name, key):
        '''Return the value for a key in a dict'''
        return self.db[name][key]

    def dgetall(self, name):
        '''Return all key-value pairs from a dict'''
        return self.db[name]

    def drem(self, name):
        '''Remove a dict and all of its pairs'''
        del self.db[name]
        self._dumpdb(self.fsave)
        return True

    def dpop(self, name, key):
        '''Remove one key-value pair in a dict'''
        value = self.db[name][key]
        del self.db[name][key]
        self._dumpdb(self.fsave)
        return value

    def dkeys(self, name):
        '''Return all the keys for a dict'''
        return self.db[name].keys()

    def dvals(self, name):
        '''Return all the values for a dict'''
        return self.db[name].values()

    def dexists(self, name, key):
        '''Determine if a key exists or not in a dict'''
        return key in self.db[name]

    def lexists(self, name, value):
        '''Determine if a value  exists in a list'''
        return value in self.db[name]

    def dmerge(self, name1, name2):
        '''Merge two dicts together into name1'''
        first = self.db[name1]
        second = self.db[name2]
        first.update(second)
        self._dumpdb(self.fsave)
        return True

    def deldb(self):
        '''Delete everything from the database'''
        self.db = {}
        self._dumpdb(self.fsave)
        return True

    def _loaddb(self):
        '''Load or reload the json info from the file'''
        self.db = simplejson.load(open(self.loco, 'rb'))

    def _dumpdb(self, forced):
        '''Write/save the json dump into the file'''
        if forced:
            simplejson.dump(self.db, open(self.loco, 'wt'))
            self.dthread = Thread(
                target=simplejson.dump,
                args=(self.db, open(self.loco, 'wt')))
            self.dthread.start()
            self.dthread.join()

