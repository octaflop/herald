#!/usr/bin/env python
# settings.py
# The main settings file
import redis

# select database. 0 is dev. 1 is production. Actually, it's just a
# convention.
DATABASE = 0
# Again, but this time with the ol' boolean
DEV = True

# Auth stuff
# CHANGE THIS TO YOUR OWN ACCORD!!!
# (Pardon my lowly import.)
from foenixauth import redispsswd, redisdns

R = redis.Redis(host=redisdns, password=redispsswd)
