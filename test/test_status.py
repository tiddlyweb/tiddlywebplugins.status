"""
Test that status returns the info we expect.
"""


from wsgi_intercept import httplib2_intercept
import wsgi_intercept
import httplib2
import shutil
import simplejson

from base64 import b64encode

from tiddlyweb import __version__ as VERSION

from tiddlyweb.config import config
from tiddlyweb.web.serve import load_app
from tiddlyweb.model.user import User
from tiddlywebplugins.utils import get_store


def setup_module(module):
    try:
        shutil.rmtree('store')
    except:  # it's not there
        pass

    app = load_app()
    def app_fn():
        return app

    module.store = get_store(config)

    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app_fn)

    module.http = httplib2.Http()


def test_simple_status():
    response, content = http.request('http://0.0.0.0:8080/status')
    assert response['status'] == '200'
    assert 'application/json' in response['content-type']
    info = simplejson.loads(content)

    assert info['username'] == 'GUEST'
    assert info['version'] == VERSION
    assert 'cookie_form' in info['challengers'][0]


def test_with_user_status():
    user = User('apple')
    user.set_password('fruit')
    store.put(user)

    authorization = b64encode('apple:fruit')

    response, content = http.request('http://0.0.0.0:8080/status',
            headers = {'Authorization': 'Basic %s' % authorization})
    assert response['status'] == '200'
    assert 'no-store' in response['cache-control']

    info = simplejson.loads(content)
    assert info['username'] == 'apple'

def test_status_as_javascript():
    response, content = http.request('http://0.0.0.0:8080/status.js')
    assert response['status'] == '200'
    assert 'text/javascript' in response['content-type']

    assert '"username": "GUEST"' in content
    assert '"version": "%s"' % VERSION in content
    assert 'var tiddlyweb = tiddlyweb || {}' in content
