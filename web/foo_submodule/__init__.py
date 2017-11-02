from .models import db
from .app import app


db.init_app(app)
