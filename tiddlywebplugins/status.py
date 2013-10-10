"""
tiddlywebplugins.status is a TiddlyWeb plugins which gives a
JSON or JavaScript report on the current state of the server
including:

* current user
* TiddlyWeb version
* available challengers

To use, add 'tiddlywebplugins.status' to 'system_plugins'
in 'tiddlywebconfig.py':

    config = {
        'system_plugins': [
            'tiddlywebplugins.status',
        ]
    }

Once running the plugin will add a route at
'{server_prefix}/status' that reports a JSON data
structure with the information described above.

If the request is made to /status.js, then the output
is the JSON encapsulated as JavaScript, so the info
can be loaded via a <script> tag in HTML. The data
ends up in the global variable 'tiddlyweb.status'.

This is primarily used to determine who is the current
TiddlyWeb user. In TiddlySpace it provides additional
information.
"""

__author__ = 'Chris Dent (cdent@peermore.com)'
__copyright__ = 'Copyright UnaMesa Association 2008-2013'
__contributors__ = ['Frederik Dohr']
__license__ = 'BSD'


try:
    import json
except ImportError:
    import simplejson as json
import tiddlyweb


def status(environ, start_response):
    """
    /status handler that retuns data as JSON.
    """
    data = _gather_data(environ)
    output = json.dumps(data)
    start_response('200 OK', [
        ('Cache-Control', 'no-store'),
        ('Content-Type', 'application/json')
    ])
    return [output]


def status_js(environ, start_response):
    """
    /status.js handler that retuns data as JavaScript,
    suitable for being loaded via a <script> tag.
    """
    data = _gather_data(environ)
    output = ('var tiddlyweb = tiddlyweb || {};\ntiddlyweb.status = %s;' %
            json.dumps(data))
    start_response('200 OK', [
        ('Cache-Control', 'no-store'),
        ('Content-Type', 'text/javascript')
    ])
    return [output]


def init(config):
    """
    Set up the status handlers.
    """
    if 'selector' in config:
        config['selector'].add('/status', GET=status)
        config['selector'].add('/status.js', GET=status_js)


def _gather_data(environ):
    """
    Create the data dictionary which will be sent in response
    to requests.
    """
    return {
            'username': environ['tiddlyweb.usersign']['name'],
            'version': tiddlyweb.__version__,
            'challengers': environ['tiddlyweb.config']['auth_systems'],
    }
