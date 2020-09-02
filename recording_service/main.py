#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import sanic
from sanic import Sanic
from sanic_cors import CORS, cross_origin
from blueprint.to_yaml import to_yaml

if __name__ == "__main__":
    app = Sanic(name="gz")
    CORS(app)
    app.blueprint(to_yaml, url_prefix='/to_yaml')
    app.run(host="0.0.0.0", port=8000, access_log=True)
