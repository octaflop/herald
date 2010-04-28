#!/usr/bin/env python

# porm.py
# PORM is a PsuedoObjectRelationalManager (ORM)
# PORM currently works on: redis

import redis
import markdown
import re
import uuid
import datetime
import pprint
#from mwlib import uparser

# app settings
from settings import DATABASE
from settings import R

# Start up redis. Vrrrrroooom...
R = redis.Redis()
# Increment ids
POSTINCR = "document:id"

# Global Methods
def unique(uid):
    """
    Checks to see if a post exists. Just in case...
    """
    if R.exists("post:%s" % uid):
        return False
    else:
        return True

def key(pid=None, uid=None, kind='global'):
    """
    A general look-up method for stuff.
    Actually, it's more of a graph between the keys.
    """
    if pid == None and uid == None:
        raise ValueError("Need a uuid or pid")
    elif isinstance(uid, uuid.UUID):
        pid = R.get("%s:%s" % (kind, uid))
        uid = R.get("%s:%i:uid" % (kind, self.pid))
    elif isinstance(uid, str):
        pid = R.get("%s:%s" % (kind, uid))
        uid = R.get("%s:%s:uid" % (kind, self.pid))
    elif isinstance(pid, int):
        uid = R.get("%s:%s:uid" % (kind, pid))
        pid = R.get("%s:%s" % (kind, self.uid))
    else:
        raise ValueError("Ok, something went wrong...")
    return (pid, uid)

def pid_from_uid(uid, kind):
    """
    Returns the pid from the uid
    """
    return R.get("%s:%s" % (kind, uid))

def graph(**args):
    """
    This is where things get interesting. The graph is a connection between
    nodes. This is an attempt to simplify this process for gettings...
    """
    raise NotImplementedError("Going to implement some modal logix")

def slugfy(text, separator='-'):
  ret = ""
  for c in text.lower():
    try:
      ret += htmlentitydefs.codepoint2name[ord(c)]
    except:
      ret += c
  ret = re.sub("([a-zA-Z])(uml|acute|grave|circ|tilde|cedil)", r"\1", ret)
  ret = re.sub("\W", " ", ret)
  ret = re.sub(" +", separator, ret)
  return ret.strip()

# Relational Models (R)
class Index(object):
    """
    An index is a sorted collection of things. This is a general class.
    TODO: I may want to make this a decorator.
    """
    def __init__(self, **kwargs):
        raise NotImplementedError("The logix is on my white board. Just want a\
                                    protoype for now.")

DEXREF = "_alpha_"
TYPELST = "global:types"

# Main models
class Document(object):
    """
    The most abstract of models, the document has key features for every post
    """
    def __init__(self, kind=None):
            self.pid = R.incr(POSTINCR)
            self.creation = datetime.datetime.now()
            self.published = False
            if not isinstance(kind, str):
                self.kind = "_document" # abstract for <document>:<id>:<attribute>
            else:
                self.kind = kind

    def post(self, container=None):
        """
        Metadata
        """
        self.incr = R.get(POSTINCR)
        self.uid = uuid.uuid1()
        assert unique(self.uid)
        self.createtime = str(datetime.datetime.now())
        R.sadd(TYPELST, self.kind)
        R.setnx("%s:%s:uid" % (self.kind, self.incr), self.uid)
        R.setnx("%s:%s" % (self.kind, self.uid), self.incr)
        R.setnx("%s:%s:publishtime" % (self.kind, self.incr), self.createtime)
        # stuff forgetting, errr, for getting.
        R.sadd(DEXREF, self.uid) # Global reference
        if not isinstance(container, str):
            container = "_meta"
        else:
            R.rpush(container, "%s:%s" % (self.kind, self.incr))
        R.rpush("global:docs", "%s:%s" % (self.incr, self.uid))

    def put(self, pid, **kwargs):
        """
        Edit a post. Takes a uid or id
        This is a wee bit messy?
        """
        self.pid, self.uid = key(pid, self.kind)
        # this is likely unsafe, but seems to be a good start
        for key in kwargs.keys():
            R.set("%s:%s:%s" % (self.kind, self.pid, key))
        modtime = str(datetime.datetime.now())
        R.rpush("%s:%s:modified" % (self.kind, self.pid), modtime)
        return True

    def get(self):
        """
        return kwargs
        this is where things get tricky...
        for now refer to str. We're just getting off the ground
        query is the biggest step.
        """
        #self.pid, self.uid = key(id)
        got = []
        for pid, kind in R.lrange("global:docs", 0, R.llen("global:docs")):
            got.append(R.get("%s:%s" % (kind, pid)))
            got.append(R.get("%s:%s:publishtime" % (kind, pid)))
        return str(got)

#    def query TODO

    def delete(self, id):
        """
        return boolean
        """
        self.pid, self.uid = key(id)

    def __str__(self):
        """
        simply dumps the server's contents
        """
        got = {}
        self.uids = R.smembers(DEXREF) # all the uids
        self.kinds = R.smembers(TYPELST) # all types of docs
        for uid in self.uids:
            got[uid] = ''
            for kind in self.kinds:
                got[uid] = [R.get("%s:%s" % (kind, uid))]
                pid = pid_from_uid(uid, kind)
                got['%s:%s' % (kind, uid)] = {
                        'kind' : kind,
                        'datetime' : R.get("%s:%s:publishtime" %\
                        (kind, pid))}
        pprint.pprint(got)


class User(Document):
    """
    The main user object
    """
    def __init__(self, username, email, fname=None, lname=None):
        self.kind = "user"
        raise NotImplementedError("class:%s is not implented." % __name__)

if __name__ == "__main__":
    def checksite():
        if R.exists(POSTINCR):
            print "Redis up and ready to go. \
                    Site implemented with incr: %i" % R.get(POSTINCR)
            return True
        else:
            R.incr(POSTINCR)
            print "Initialized to: %i" % R.get(POSTINCR)
            return True
    checksite()

