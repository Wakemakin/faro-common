import unittest

import flask

import faro_common.flask as flaskutils


class FlaskTest(unittest.TestCase):

    def create_flask_app(self):
        app = flaskutils.make_json_app(flask.Flask("testing_app"))

        @app.route("/")
        def test():
            return "10"

        @app.route("/requirebody", methods=['GET', 'POST'])
        @flaskutils.require_body
        def body_required():
            return "10"

        @app.route("/withoutcors")
        def not_cross_domain():
            return "10"

        @app.route("/withcors")
        @flaskutils.crossdomain(origin="*")
        def cross_domain():
            return "10"

        @app.route("/testjsonify", methods=['POST'])
        def json_stuff():
            flaskutils.json_request_data(flask.request.data)

        return app

    def setUp(self):
        self.app = self.create_flask_app()
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_require_body(self):
        rv = self.client.post('/requirebody', data=None, follow_redirects=True)
        assert rv.status_code == 400
        rv = self.client.post('/requirebody', data={}, follow_redirects=True)
        assert rv.status_code == 400
        rv = self.client.post('/requirebody', data='', follow_redirects=True)
        assert rv.status_code == 400

    def test_json_request_data(self):
        rv = self.client.post('/testjsonify', data="asdf",
                              follow_redirects=True)
        assert rv.status_code == 400
        rv = self.client.post('/testjsonify', data="{asdf: 'a'}",
                              follow_redirects=True)
        assert rv.status_code == 400

    def test_cors(self):
        rv = self.client.options('/withoutcors')
        assert 'Access-Control-Allow-Origin' not in rv.headers
        assert 'Access-Control-Allow-Methods' not in rv.headers
        assert 'Access-Control-Max-Age' not in rv.headers
        rv = self.client.options('/withcors')
        assert 'Access-Control-Allow-Origin' in rv.headers
        assert 'Access-Control-Allow-Methods' in rv.headers
        assert 'Access-Control-Max-Age' in rv.headers
        rv = self.client.options('/mistake')
        assert rv.status_code == 404
