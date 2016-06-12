from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException, default_exceptions


def make_json_app(import_name, **kwargs):
    """
    Creates a JSON-oriented Flask app.
    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):
    { "Err": "405: Method Not Allowed" }
    """
    def make_json_error(ex):
        response = jsonify({"Err": str(ex)})
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    wrapped_app = Flask(import_name, **kwargs)

    for code in default_exceptions.iterkeys():
        wrapped_app.errorhandler(code)(make_json_error)

    return wrapped_app
