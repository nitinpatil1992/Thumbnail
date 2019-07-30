import pytest

from webtest import TestApp

from gazo.api import create_app
from gazo.settings import TestConfig

@pytest.yield_fixture(scope='function')
def app():
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()
    yield _app
    ctx.pop()

@pytest.fixture(scope='function')
def testapp(app):
    return TestApp(app)
