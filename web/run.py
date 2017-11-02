#!/usr/bin/env python

"""Run the webserver."""

from foo_submodule import app, db

if __name__ == "__main__":
    app.debug = True
    # Because we did not initialize Flask-SQLAlchemy with an application
    # it will use `current_app` instead.  Since we are not in an application
    # context right now, we will instead pass in the configured application
    # into our `create_all` call.
    db.create_all(app=app)
    from gevent.wsgi import WSGIServer
    http_server = WSGIServer(('', 8082), app)
    http_server.serve_forever()
