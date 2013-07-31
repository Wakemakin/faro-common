import datetime
import functools
import json

import flask
import flask.ext.jsonpify as jsonp
import werkzeug.exceptions as http

import faro_common.exceptions.common as exc


def make_json_app(app, **kwargs):
    def make_json_error(ex):
        if hasattr(ex, "information"):
            response = jsonp.jsonify(message=str(ex),
                                     information=ex.information)
        else:
            response = jsonp.jsonify(message=str(ex))
        response.status_code = (ex.code
                                if isinstance(ex, http.HTTPException)
                                else 500)
        return response

    for code in http.default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error

    return app


def require_body(func):
    def check_body_exists(*args, **kwargs):
        if len(flask.request.data) == 0:
            raise exc.RequiresBody()
        return func(*args, **kwargs)
    return check_body_exists


def json_request_data(request_data):
    try:
        if request_data == '{}':
            return None
        return json.loads(request_data)
    except ValueError:
        raise exc.InvalidInput(information="Malformed body")


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, datetime.timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = flask.current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and flask.request.method == 'OPTIONS':
                resp = flask.current_app.make_default_options_response()
            else:
                resp = flask.make_response(f(*args, **kwargs))
            if not attach_to_all and flask.request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        f.required_methods = ['OPTIONS']
        return functools.update_wrapper(wrapped_function, f)
    return decorator
