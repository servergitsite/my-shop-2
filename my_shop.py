import os
import sqlite3
from flask import render_template
from flask import Flask, jsonify
from flask import request
from werkzeug.utils import secure_filename


app = Flask(__name__)


@app.route('/latest_item')
def latest_item():
    data = {"description": "TODO", "price": 12.34}
    return jsonify(data)


@app.route('/my_shop/')
@app.route('/my_shop/<name>')
def my_shop(name=None):
    return render_template('my_shop.html', name=name)


@app.route('/my_shop_2/')
@app.route('/my_shop_2/<name>')
def my_shop_2(name=None):
    return render_template('my_shop_dynamic.html', name=name)


@app.route('/items', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        img_upload_dir = "/Users/family/dev/noah_shop/static"
        f = request.files['my_file']

        if f:
            print("-------> file found in request")
        else:
            print("---------> no file in request")

        # TODO: add support for other filetypes (.jpg, etc.)
        # image_filename = os.path.join(img_upload_dir, "latest_item.png")
        image_filename = os.path.join(img_upload_dir, secure_filename(f.filename))
        f.save(image_filename)


        # TODO: Create the DB connection at app startup

        # Connect to the database
        print("\n\n-----------> connecting...")
        db_path = "/Users/family/dev/noah_shop/my_shop.db"
        conn = sqlite3.connect(db_path)
        curr = conn.cursor()

        # Prepare the SQL query
        sql_query = '''
        INSERT INTO item (image_filename, description, price)
        VALUES (?, ?, ?)
        '''

        description = request.form.get('item_description', 'No description')
        price = request.form.get('price', 0.00)

        try:
            new_row = (image_filename, description, float(price))
            curr.execute(sql_query, new_row)
            conn.commit()
        except ValueError:
            print(f"Price not valid: {price}")

        return render_template('item_added.html', name=None)
    elif request.method == 'GET':
        return render_template('add_item.html', name=None)
