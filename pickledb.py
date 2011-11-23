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

import json

    

def load(location, option):
    '''Return a pickledb object. location is the path to the json file.'''
    return pickledb(location, option)

class pickledb(object):

    def __init__(self, location, option):
        '''Creates a database object and loads the data from the location path.
        If the file does not exist it will be created on the first update.'''
        self.load(location, option)
    
    def load(self, location, option):
        '''Loads, reloads or changes the path to the db file.
        Do not use this method has it may be deprecated in the future.'''
        self.loco = location
        self.fsave = option
        try:
            self._loaddb()
        except IOError:
            self.db = {}
        return True
    
    def dump(self):
        '''Force dump memory db to file. a new location may be set at dump time'''
        self._dumpdb(True)
        return True
    
    def set(self, key, value):
        '''Set the string value of a key'''
        # FIXME does not confirm value type
        # http://redis.io/commands/set
        self.db[key] = value
        self._dumpdb(self.fsave)
        return True
    
    def get(self, key):
        '''Get the value of a key'''
        # FIXME Redis docs say this should be a string
        # http://redis.io/commands/get
        try:
            return self.db[key]
        except KeyError:
            return None
    
    def rem(self, key):
        '''Delete a key'''
        del self.db[key]
        self._dumpdb(self.fsave)
        return True
    
    def lcreate(self, name):
        '''Create a list'''
        self.db[name] = []
        self._dumpdb(self.fsave)
        return True
    
    def ladd(self, name, value):
        '''Add a value to a list'''
        self.db[name].append(value)
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
        # FIXME should return the number of removed keys
        # http://redis.io/commands/lrem
        del self.db[name]
        self._dumpdb(self.fsave)
        return True
    
    def lpop(self, name, pos):
        '''Remove one value in a list'''
        # FIXME should return the deleted value
        # http://redis.io/commands/lpop
        del self.db[name][pos]
        self._dumpdb(self.fsave)
        return True
    
    def llen(self, name):
        '''Returns the length of the list'''
        # FIXME should return 0 if there is no list
        # http://redis.io/commands/llen
        return len(self.db[name])
    
    def append(self, key, more):
        '''Add more to a key's value'''
        # FIXME should return the length of the string
        # http://redis.io/commands/append
        tmp = self.db[key]
        self.db[key] = ('%s%s' % (tmp, more))
        self._dumpdb(self.fsave)
        return True
    
    def lappend(self, name, pos, more):
        '''Add more to a value in a list'''
        # FIXME return the length akin to append()
        tmp = self.db[name][pos]
        self.db[name][pos] = ('%s%s' % (tmp, more))
        self._dumpdb(self.fsave)
        return True
    
    def dcreate(self, name):
        '''Create a dict'''
        self.db[name] = {}
        self._dumpdb(self.fsave)
        return True
    
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
        '''Remove one key-value in a dict'''
        # FIXME return deleted value
        del self.db[name][key]
        self._dumpdb(self.fsave)
        return True
    
    def deldb(self):
        '''Delete everything from the database'''
        self.db= {}
        self._dumpdb(self.fsave)
        return True
    
    def _loaddb(self):
        '''Load or reload the json info from the file'''
        self.db = json.load(open(self.loco, 'rb'))
    
    def _dumpdb(self, forced):
        '''Dump (write, save) the json dump into the file'''
        # FIXME only forced dumps happen
        # should allow users to set automatic dumps
        if forced:
            json.dump(self.db, open(self.loco, 'wb'))
