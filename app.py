import os
import csv
from flask import Flask, render_template, request, redirect, jsonify
import requests

from config import DevelopmentConfig, ProductionConfig
from consts import INSTANCE_PATH
from colour import ColourRGB, gradient
from db.models import db, Breeds, Images


app = Flask(__name__)
app.config.from_object(ProductionConfig())
db.init_app(app)

url = 'https://www.googleapis.com/customsearch/v1'


@app.cli.command('create-database')
def create_database():
    db_fldr = os.path.join(INSTANCE_PATH, 'db')

    breed_count = db.session.query(Breeds).count()
    if breed_count == 0:
        print('Initialising database')
        with open(os.path.join(db_fldr, 'breeds.csv'), 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            skip_header = True
            for row in reader:
                if skip_header:
                    skip_header = False
                else:
                    breed = Breeds(row[0], row[1], 0)
                    db.session.add(breed)

        db.session.commit()
        print('breeds table has been populated')
    else:
        print(f'breeds table already populated with {breed_count} rows')


@app.route('/')
def main():
    # Get a random dog which has minimal search count
    stmt = db.text("""SELECT id, breed, query, search_count FROM breeds WHERE id IN (
        SELECT top 1 (id)
        FROM breeds
        WHERE search_count = (SELECT min(search_count) FROM breeds)
        ORDER BY NEWID()
    );""")
    result = db.session.execute(stmt)
    (breed_id, breed_name, query, search_count) = result.fetchone()

    # Submit an API request for that dog
    payload = {
        'cx': os.getenv('GOOGLE_CX_KEY'),
        'key': os.getenv('GOOGLE_API_KEY'),
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

    # Render a template using the data from the API
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

    # Add image urls to database
    for box in [x for x in data if x.startswith('box_')]:
        img = Images(breed_id, data[box])
        db.session.add(img)

    # Commit changes
    db.session.commit()

    return redirect('/')


@app.route('/progress')
def progress():
    img_count = db.session.query(Images).count()
    prop = max(min(img_count / 95000, 1), 0)

    target_colour = gradient(prop, ColourRGB(255, 0, 0), ColourRGB(0, 255, 0))
    colour_hex = target_colour.hex()

    return render_template('progress.html', count=img_count, percent=f'{prop*100:.2f}%', colour=colour_hex)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    db.create_all()
    app.run()
