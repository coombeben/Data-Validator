import os
import csv
from flask import Flask, render_template, request, redirect

from config import DevelopmentConfig, ProductionConfig
from consts import INSTANCE_PATH
from colour import ColourRGB, gradient
from db.models import db, Breeds, Images, Staging


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
    stmt = db.text("""SELECT TOP 10 b.id, b.breed, s.staging_id, s.url
        FROM breeds b
        LEFT JOIN staging s ON b.id = s.breed_id
        WHERE s.breed_id = (
            SELECT top 1 (id)
            FROM breeds
            WHERE (search_count + offset) = (SELECT min(search_count + offset) FROM breeds)
            ORDER BY NEWID()
        );""")
    result = db.session.execute(stmt)

    data = result.fetchall()

    if data is None:
        return 'No images available at this time'

    breed_id = data[0][0]
    breed_name = data[0][1]
    img_ids = [x[2] for x in data]
    img_urls = [x[3] for x in data]

    return render_template('main.html', breed_name=breed_name, breed_id=breed_id, img_urls=img_urls, img_ids=img_ids)


@app.route('/handle_response', methods=['POST'])
def handle_response():
    # Read input data
    data = request.form.to_dict()
    breed_id = data['breed_id']
    img_ids = data['img_ids'][1:-1].split(', ')

    # Increase search_count counter
    breed = db.session.query(Breeds).filter(Breeds.id == breed_id).first_or_404()
    breed.search_count = breed.search_count + 1

    # Add image urls to database
    for box in [x for x in data if x.startswith('box_')]:
        img = Images(breed_id, data[box])
        db.session.add(img)
        # TODO: db.session.add_all()

    # Delete from staging
    for staging_id in img_ids:
        db.session.query(Staging).where(Staging.staging_id == staging_id).delete()

    # Commit changes
    db.session.commit()

    return redirect('/')


@app.route('/progress')
def progress():
    img_count = db.session.query(Images).count() + 20105
    prop = max(min(img_count / 79800, 1), 0)

    target_colour = gradient(prop, ColourRGB(255, 0, 0), ColourRGB(0, 255, 0))
    colour_hex = target_colour.hex()

    return render_template('progress.html', count=img_count, percent=f'{prop*100:.2f}%', colour=colour_hex)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    db.create_all()
    app.run()
