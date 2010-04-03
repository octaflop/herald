from bottle import run, route, view, send_file, debug, template, validate, request, post
import redis
import bottle

#redis referent
r = redis.Redis()

#static routing for css and js
@route('/static/:filename')
def static_file(filename):
    send_file(filename, root='/static/')

@route('/')
def index():
    return dict(title=title, menu=menu, posts=posts)

if __name__ == "__main__":
    import bottle
    #bottle debug
    bottle.debug(True)
    #run(host="0.0.0.0", port=8080, refresh=True)
    run(host="0.0.0.0", port=8080)
