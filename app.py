"""
Herald is a blogging app with a redis backend.
"""
__author__ = 'Faris Chebib'
__version__ = '0.0.1'
__license__ = 'BSD'

from bottle import run, route, view, send_file, debug, template, validate, request, post, response
import redis
import bottle
import os
import datetime

#redis referent
r = redis.Redis()

# site id. 1 is dev. 0 is production.
SID = 1

#static routing for css and js
@route('/static/:filename#.*#')
def static_file(filename):
    send_file(filename, root=os.getcwd() + '/static')

#Dynamic Shit
@route('/')
@view('home.tpl')
def index():
    """Returns the index with the 10 latest posts"""
    title = "test"
    menu = "menu"
    posts = []
    maxr = r.zcard("site:%i:posts" % SID)
    posts = r.zrange("site:%i:posts" % SID, maxr, (maxr - 10))
    return dict(title=title, menu=menu, posts=posts, maxr=maxr)

@route('/post/new/:id')
@validate(id=int)
@view('edit_post.tpl')
def post_new(id):
   """
   Create a new post based on id
   """
   timestamp = datetime.datetime.isoformat(datetime.datetime.now())
   id = id
   return dict(id=id, timestamp=timestamp)

@route('/post/do', method='POST')
def post_post():
    """
    Post the form
    """
    id = request.POST.get('id', '').strip()
    if not id: # should be int, but isn't
        return "What the hell, man?"
    else:
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        date = request.POST.get('timestamp', '').strip()
        r.set("post:%s:title" % id, title)
        r.set("post:%s:content" % id, content)
        r.set("post:%s:date" % id, date)
        r.zadd("site:%s:posts" % SID, "post:%s" % id, 1)
        titler = r.get("post:%s:title" % id)
        return "Success! %s has been posted as %s !" % (title, titler)

@route('/post/:postid')
#@route('/:year/:month/:day/:postid')
@validate(postid=int)
@view('post.tpl')
def post(postid, year=0, month=0, day=0):
    """Returns a single post. Date is optional"""
    title = str(r.get("post:%s:title" % postid))
    if not title:
        return dict(title="what the fuck")
    else:
        content = str(r.get("post:%s:content" % postid))
        date = str(r.get("post:%s:date" % postid))
        pid = str(postid)
        return dict(title=title, content=content, date=date, pid=pid)

# TODO
@route('/:year/:month/:day/')
def post(year, month, day):
    """Returns all posts for a given day"""
    return dict(title=title, content=content, date=date)

@route('/:year/:month/')
def post(year, month):
    """Returns all posts for a given month"""
    return dict(title=title, content=content, date=date)

@route('/:year/')
def post(year):
    """Returns all posts for a given year"""
    return dict(title=title, content=content, date=date)

if __name__ == "__main__":
    bottle.debug(True)
    bottle.run(host="0.0.0.0", port=8080)
