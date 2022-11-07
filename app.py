import os
from flask import Flask, render_template, request, redirect, jsonify
from flask_migrate import Migrate
import requests

from config import DevelopmentConfig, ProductionConfig
from db.models import db, Breeds, Images
from db.database_setup import populate_database


app = Flask(__name__)
app.config.from_object(ProductionConfig())
db.init_app(app)
migrate = Migrate(app, db)

url = 'https://www.googleapis.com/customsearch/v1'


@app.cli.command('create-database')
def create_database():
    populate_database()


@app.route('/')
def main():
    stmt = db.text("""SELECT id, breed, query, search_count FROM breeds WHERE id IN (
        SELECT id
        FROM breeds
        WHERE search_count = (SELECT min(search_count) FROM breeds)
        ORDER BY random()
        LIMIT 1
    );""")
    result = db.session.execute(stmt)
    (breed_id, breed_name, query, search_count) = result.fetchone()

    payload = {
        'cx': '3745ad675cafd4f33',
        'key': 'AIzaSyCqnp2MjliHaH2BcCEHKiQl20CS04uccSE',
        'q': query,
        'searchType': 'image',
        'imgType': 'photo',
        'fields': 'items(link)',
        'filter': '1',
        'start': 10 * search_count + 1
    }
    response = requests.get(url, params=payload)

    if response.status_code != 200:
        render_template('error.html', err_msg=response.text)

    data = response.json()
    images = [x['link'] for x in data['items']]

    return render_template('main.html', breed_name=breed_name, images=images, breed_id=breed_id)


@app.route('/handle_response', methods=['POST'])
def handle_response():
    data = request.form.to_dict()
    breed_id = data['breed_id']

    # Increase search_count counter
    breed = db.session.query(Breeds).filter(Breeds.id == breed_id).first_or_404()
    breed.search_count = breed.search_count + 1
    db.session.commit()

    # Add image urls to database
    for box in [x for x in data if x.startswith('box_')]:
        img = Images(breed_id, data[box])
        db.session.add(img)
        db.session.commit()

    return redirect('/')


@app.route('/api/get_breed')
def get_breed():
    breed_id = request.args.get('id')
    return_breeds = db.session.query(Breeds).filter(Breeds.id == int(breed_id)).first()
    json_data = {
        'id': return_breeds.id,
        'breed': return_breeds.breed,
        'query': return_breeds.query,
        'search_count': return_breeds.search_count
    }
    return jsonify(json_data)


@app.route('/api/get_imgs')
def get_img():
    breed_id = request.args.get('id')
    return_imgs = db.session.query(Images).filter(Images.breed_id == int(breed_id)).all()
    json_data = [{
        'id': img.id,
        'breed_id': img.breed_id,
        'url': img.url
    } for img in return_imgs]
    return jsonify(json_data)


if __name__ == '__main__':
    db.create_all()
    app.run()
