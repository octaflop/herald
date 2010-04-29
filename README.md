Herald is a simple blogging platform written in python.
The web-library used to create herald is bottle.py. The database is based
on the NoSQL database redis, and redis-python is used to make the calls.

This project is currently in early alpha stages, and is not intended for use in
any production environment. It has no user authentication or session-support.
These are all in the works. 

As of version 0.3, the Psuedo-Object Relational Manager is running. It has
support for basic getting and setting, but no support for Queries (yet). 

To run the app, simply start up your redis-server and start the app with 
    python app.py

Other fun things to try: 
* Import the orm and use it define your own document classes
* Match the [mongoengine](http://hmarr.com/mongoengine/) api to the orm api.
* Implement sessions in redis.

TODO:
* Incorporate the new orm with the main app
* Re-write the url-mappers
* Build admin templates
