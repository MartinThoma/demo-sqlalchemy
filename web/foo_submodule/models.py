#!/usr/bin/env python

"""Models which represent tables in the database."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Foobar(db.Model):
    """Model for Foobar."""

    __tablename__ = 'foobar'
    foo = db.Column(db.Integer, primary_key=True)
    bar = db.Column(db.Integer)

    def __init__(self, bar):
        self.bar = bar

    def __repr__(self):
        """Return a representation of this object."""
        return "<Foobar({}, {})>".format(self.foo, self.bar)
