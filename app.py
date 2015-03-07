#!/usr/bin/env python
#*-* coding: utf-8 *-*
# Local server will attempt to run using Werkzeug first if available, or
# will fail to a generic WSGIServer. Werkzeug offers niceties like a
# a debugging console and autorealoder.
from brainstorm import main
from ConfigParser import SafeConfigParser
import os

parser = SafeConfigParser({'here': os.path.dirname(os.path.abspath(__file__))})
parser.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini'))
config = dict(parser.items('app:main'))

application = main(**config)
