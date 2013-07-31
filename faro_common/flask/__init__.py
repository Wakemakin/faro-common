import flask.ext.jsonpify as jsonp
import werkzeug.exceptions as http


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
