import random
"""
Here's kinda what I'd like to do:

r.zadd("site:%s" % id, (r.lrange("post:%s:comment" % id, 0, 0)), 1)
# or
r.zadd("site:%s" % site_id, (r.lrange("post:%s:comment" % id, 0, # key 
(r.get("global:settings:maxfrontcomments")), # max range
(r.get("post:%s:rank" % id))) # incr rank in cardinal list by a pulled amount

ID: <year>.<month>.<day>.<incr>.<time>
ex: 2010.04.24.1.232505

Site will need a unique hash. Script will initiate through a "site" list with a
hashed id.
"""
class Post(object):
    def __init__(self, title, content, imageref, author)
        self.author = author
        self.title = title
        self.content = content
        self.datepub = datetime.datetime.now()

    def __repr__():
        # return something

    def new():
        # make a new post

    def del():
        # delete a post

    def edit():
        # edit a post

class User(object):
    def __init__:
        self.name = name
        self.password = password
        self.
    def new():
        # make a new post

    def del():
        # delete a post

    def edit():

class Comment
