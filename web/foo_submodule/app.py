#!/usr/bin/env python

"""Service for table extraction."""

# Core Library modules
import locale
import logging.handlers
import os

# Third party modules
import config
import models
from flask import Flask, render_template
from models import db

# Local modules
from .config import cfg

__version__ = "0.1.0"


SQLALCHEMY_DATABASE_URI = (
    "mysql://{username}:{password}@{host}:{port}/"
    "{dbname}?charset=utf8".format(
        username=config.cfg["db"]["username"],
        password=config.cfg["db"]["password"],
        dbname=config.cfg["db"]["dbname"],
        port=config.cfg["db"]["port"],
        host=config.cfg["db"]["host"],
    )
)


# Create app
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
app = Flask(__name__, template_folder="template", static_folder="static")
app.config["UPLOAD_FOLDER"] = cfg["upload_dir"]
print("UPLOAD_FOLDER={}".format(app.config["UPLOAD_FOLDER"]))
app.secret_key = "super secret key"
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SQLALCHEMY_POOL_SIZE"] = 2
app.config["SQLALCHEMY_MAX_OVERFLOW"] = 3
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = True
app.url_map.strict_slashes = False
db.init_app(app)


def configure_logger(logger):
    """Configure a logger object with logfile rotation."""
    log_filename = os.path.join(config.cfg["upload_dir"], "web-service.log.txt")

    if len(logger.handlers) <= 2:
        logger.setLevel(logging.DEBUG)

        # Add the log message handler to the logger
        max_bytes = 10 * 1024 * 1024
        handler = logging.handlers.RotatingFileHandler(
            log_filename, maxBytes=max_bytes, backupCount=5
        )
        handler.setLevel(logging.DEBUG)

        # create formatter and add it to the handlers
        log_format_string = "%(asctime)s %(levelname)s - %(message)s"
        formatter = logging.Formatter(log_format_string)
        handler.setFormatter(formatter)
        logger.addHandler(handler)


configure_logger(app.logger)


@app.teardown_request
def teardown_request(exception):
    """
    Do this if an exception happens.

    Notes
    -----
    https://stackoverflow.com/a/33284980/562769
    """
    if exception:
        db.session.rollback()
        db.session.remove()
    db.session.remove()


@app.route("/")
def main():
    """Show all foobar."""
    from random import randint

    me = models.Foobar(randint(0, 1000))
    db.session.add(me)
    db.session.commit()
    data = models.Foobar.query.order_by(models.Foobar.foo).all()
    return render_template("home.html", data=data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", threaded=True)
