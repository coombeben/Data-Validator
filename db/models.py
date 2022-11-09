from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Breeds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    breed = db.Column(db.String(64), nullable=False)
    query = db.Column(db.String(64), nullable=False)
    search_count = db.Column(db.Integer, nullable=False)

    def __init__(self, breed, query, search_count=0):
        self.breed = breed
        self.query = query
        self.search_count = search_count


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    breed_id = db.Column(db.Integer, db.ForeignKey('breeds.id'), nullable=False)
    url = db.Column(db.String(1024))
    downloaded = db.Column(db.Boolean, nullable=False)

    def __init__(self, breed_id, url, downloaded=False):
        self.breed_id = breed_id
        self.url = url
        self.downloaded = downloaded
