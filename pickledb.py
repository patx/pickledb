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

class pickledb(object):
    def __init__(self, location):
        self.load(location)
    
    def load(self, location):
        self.loco = location
        try:
            self._loaddb()
        except IOError:
            self.db = {}
        return True

    def set(self, key, value):
        self.db[key] = value
        self._dumpdb()
        return True
    
    def get(self, key):
        try:
            return self.db[key]
        except KeyError:
            return None
    
    def rem(self, key):
        del self.db[key]
        self._dumpdb()
        return True
    
    def lcreate(self, name):
        self.db[name] = []
        self._dumpdb()
        return True
    
    def ladd(self, name, value):
        self.db[name].append(value)
        self._dumpdb()
        return True
    
    def lgetall(self, name):
        return self.db[name]
    
    def lget(self, name, pos):
        return self.db[name][pos]
    
    def lrem(self, name):
        del self.db[name]
        self._dumpdb()
        return True
    
    def lpop(self, name, pos):
        del self.db[name][pos]
        self._dumpdb()
        return True
    
    def llen(self, name):
        return len(self.db[name])
    
    def append(self, key, more):
        tmp = self.db[key]
        self.db[key] = ('%s%s' % (tmp, more))
        self._dumpdb()
        return True
    
    def lappend(self, name, pos, more):
        tmp = self.db[name][pos]
        self.db[name][pos] = ('%s%s' % (tmp, more))
        self._dumpdb()
        return True
    
    def dcreate(self, name):
        self.db[name] = {}
        self._dumpdb()
        return True
    
    def dadd(self, name, pair):
        self.db[name][pair[0]] = pair[1]
        self._dumpdb()
        return True
    
    def dget(self, name, key):
        return self.db[name][key]
    
    def dgetall(self, name):
        return self.db[name]
    
    def drem(self, name):
        del self.db[name]
        self._dumpdb()
        return True
    
    def dpop(self, name, key):
        del self.db[name][key]
        self._dumpdb()
        return True
    
    def flushdb(self):
        self.db={}
        self._dumpdb()
        return True
    
    def _loaddb(self):
        self.db = json.load(open(self.loco, 'rb'))
    
    def _dumpdb(self):
        json.dump(self.db, open(self.loco, 'wb'))
    

def load(location):
    return pickledb(location)