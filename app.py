from bottle import run, route, view, send_file, debug, template, validate, request, post
import redis
import bottle
import os

#redis referent
r = redis.Redis()

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
    posts = "poster"
    return dict(title=title, menu=menu, posts=posts)

@route('/post/:postid')
@route('/:year/:month/:day/:postid')
def post(postid, year=0, month=0, day=0):
    """Returns a single post. Date is optional"""
    return dict(title=title, content=content, date=date)

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
    import bottle
    #bottle debug
    bottle.debug(True)
    #run(host="0.0.0.0", port=8080, refresh=True)
    run(host="0.0.0.0", port=8080)
