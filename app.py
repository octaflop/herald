# -*- coding: utf-8 -*-
"""
Herald is a blogging app with a redis backend.
"""
__author__ = 'Faris Chebib'
__version__ = '0.0.1'
__license__ = 'BSD'

from bottle import run, route, view, send_file, debug, template, validate,\
request, post, response, redirect, abort
import redis, bottle, os, datetime, htmlentitydefs, re, hashlib
from beaker.middleware import SessionMiddleware
from bottle import CherryPyServer

# from bottle faq
session_opts = {
    'session.type': 'file',
    'session.cookies_expires': 300,
    'session.data_dir': './cache',
    'session.auto': True
    }


#redis referent
r = redis.Redis()

# site id. 1 is dev. 0 is production.
SID = 1

#static routing for css and js
@route('/static/:filename#.*#')
def static_file(filename):
    send_file(filename, root=os.getcwd() + '/static')

@route('/favicon.ico')
def favicon():
    send_file('favicon.ico', root=os.getcwd() + '/static')

#Dynamic Shit
@route('/')
@view('home.tpl')
def index():
    """Returns the index with the 10 latest posts"""
    title = "test"
    menu = ["menuitem1", "menuitem2"]
    posts_headlines, posts_links = [], []
    postsind = r.zrange("site:%i:posts" % SID, 0, -1)
    for ii in range(0,len(postsind)):
        posts_headlines.append(r.get("%s:title" % postsind[ii]))
        posts_links.append(r.get("%s:urlslug" % postsind[ii]))
    posts = zip(posts_headlines, posts_links)
    return dict(title=title, menu=menu, posts=posts)

@route('/post/new')
@view('edit_post.tpl')
def post_new():
    """
    Create a new post
    """
    year, month, day, hour, minute, second = datetime.datetime.now().year,\
    datetime.datetime.now().month, datetime.datetime.now().day,\
    datetime.datetime.now().hour,datetime.datetime.now().minute,\
    datetime.datetime.now().second
    timestamp = "%i.%i.%i_%i:%i:%i" % (year, month, day, hour, minute, second)
    return dict(timestamp=timestamp)

def crunch(year, month, day, title):
    return hashlib.sha512(str(year) + str(month) + str(day) + title).hexdigest()

@route('/post/do', method='POST')
def post_post():
    """
    Post the form
    """
    title = request.POST.get('title', '').strip()
    if not title: # should be int, but isn't
        return "What the hell, man? No title."
    else:
        content = request.POST.get('content', '').strip() # need to validate?
        date = request.POST.get('timestamp', '').strip()
        pid = r.incr('global:pid') # unique post id
        year, month, day, hour, minute, second = datetime.datetime.now().year,\
        datetime.datetime.now().month, datetime.datetime.now().day,\
        datetime.datetime.now().hour,datetime.datetime.now().minute,\
        datetime.datetime.now().second
        urlslug = "/%i/%i/%i/%s" % (year, month, day, slugfy(title))
        r.set("post:%s:title" % pid, title)
        r.set("post:%s:content" % pid, markdown.markdown(content))
        r.set("post:%s:date" % pid, date)
        r.set("post:%s:urlslug" % pid, urlslug)
        r.set("post:%s:digest" % pid, crunch(year, month, day, slugfy(title)))
        r.set("digest:%s" % crunch(year, month, day, slugfy(title)), pid)
        r.zadd("site:%s:posts" % SID, "post:%s" % pid, 1)
        return redirect(urlslug)

@route('/post/:pid/edit')
@validate(pid=int)
def post_post(pid):
    """
    Edit a post
    """
    title = r.get('post:%s:title' % pid)
    if not title: # should be int, but isn't
        return "PID not found"
    else:
        content = request.POST.get('content', '').strip() # need to validate?
        date = request.POST.get('timestamp', '').strip()
        pid = r.incr('global:pid') # unique post id
        year, month, day, hour, minute, second = datetime.datetime.now().year,\
        datetime.datetime.now().month, datetime.datetime.now().day,\
        datetime.datetime.now().hour,datetime.datetime.now().minute,\
        datetime.datetime.now().second
        urlslug = "/%i/%i/%i/%s" % (year, month, day, slugfy(title))
        r.set("post:%s:title" % pid, title)
        r.set("post:%s:content" % pid, markdown.markdown(content))
        r.set("post:%s:date" % pid, date)
        r.set("post:%s:urlslug" % pid, urlslug)
        r.set("post:%s:digest" % pid, crunch(year, month, day, slugfy(title)))
        r.set("digest:%s" % crunch(year, month, day, slugfy(title)), pid)
        r.zadd("site:%s:posts" % SID, "post:%s" % pid, 1)
        return redirect(urlslug)

def get_id_from_url(year, month, day, slug):
    pid = r.get("digest:%s" % crunch(year, month, day, slug))
    if not r.get("post:%s:digest" % pid) == crunch(year, month, day, slug):
        return abort(404)
    else:
        return pid

@route('/post/:postid')
@validate(postid=int)
@route('/:year/:month/:day/:slug')
@validate(year=int,month=int,day=int,slug=str)
@view('post.tpl')
def post(postid=None, year=None, month=None, day=None, slug=None):
    """Returns a single post. Date is optional"""
    if postid:
        pid = postid
        url = r.get("post:%s:urlslug" % pid)
        return redirect(url)
    else:
        pid = get_id_from_url(year, month, day, slug)
    title = str(r.get("post:%s:title" % pid))
    content = str(r.get("post:%s:content" % pid))
    date = str(r.get("post:%s:date" % pid))
    return dict(title=title, content=content, date=date, pid=pid)

# TODO
#@route('/:year/:month/:day/')
def post(year, month, day):
    """Returns all posts for a given day"""
    return dict(title=title, content=content, date=date)

#@route('/:year/:month/')
def post(year, month):
    """Returns all posts for a given month"""
    return dict(title=title, content=content, date=date)

#@route('/:year/')
def post(year):
    """Returns all posts for a given year"""
    return dict(title=title, content=content, date=date)

if __name__ == "__main__":
    bottle.debug(True)
    bottle.run(host="0.0.0.0", port=8080, server=CherryPyServer)
