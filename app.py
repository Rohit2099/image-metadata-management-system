from flask import Flask, render_template, session, redirect, url_for, request
from pymongo import MongoClient
import pprint
from pymongo import MongoClient
from PIL import Image
from PIL.ExifTags import TAGS
import os
import base64
import json
import time
import io

app = Flask(__name__)
client = MongoClient('52.146.82.229', 27017)

db = client.CloudComp
collection = db['Webapp']


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        session['user'] = request.form['username']
        session['pass'] = request.form['password']
        if session['user'] == 'guest' and session['pass'] == 'guest':
            return render_template('query_upload.html')
        else:
            return render_template('login.html')


@app.route('/start')
def start():
    if 'user' in session and session['user'] == 'guest' and 'pass' in session and session['pass'] == 'guest':
        return render_template('start.html')
    else:
        return render_template('login.html', items = 1)


@app.route('/goback', methods=['POST'])
def goback():
    if 'user' in session and session['user'] == 'guest' and 'pass' in session and session['pass'] == 'guest':
        return render_template('query_upload.html')
    else:
        return render_template('login.html', items = 1)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if 'user' in session and session['user'] == 'guest' and 'pass' in session and session['pass'] == 'guest':
        if request.method == "POST":
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                try:
                    image = Image.open(uploaded_file)

                    img = Image.open(uploaded_file, mode='r')
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()

                    encoded_string = str(base64.b64encode(img_byte_arr))
                    print(type(encoded_string))
                    exif = {
                        TAGS[k]: str(v)
                        for k, v in image.getexif().items()
                        if k in TAGS
                    }
                    exif['file_encoded'] = encoded_string
                    collection.insert_one(exif)
                    result = []
                    result.append(exif)
                    return render_template('results.html', items = result)
                except:
                    return "<h4>Error uploading the image</h4>"
            else:
                return render_template('upload.html', items=0)
        else:
            return render_template('upload.html')
    
    else:
        return render_template('login.html', items = 1)


@app.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        if 'user' in session:
            session.pop('user', None)
        if 'pass' in session:
            session.pop('pass', None)
        return render_template('login.html')


@app.route('/retrieveImage', methods=['GET', 'POST'])
def retrieve():
    if 'user' in session and session['user'] == 'guest' and 'pass' in session and session['pass'] == 'guest':
        if request.method == 'POST':
            return render_template('start.html')
        
        make = request.args['make']
        fnumber = request.args['FNumber']
        imgHeight = request.args['Height']
        imgWidth = request.args['Width']

        query_results = list(collection.find({'Make': make, 'FNumber': fnumber, 'ExifImageHeight':imgHeight, 'ExifImageWidth': imgWidth}))
        return render_template('results.html', items=query_results)
    else:
        return render_template('login.html', items = 1)


if __name__ == '__main__':
    app.secret_key = 'jebfiuwbeiueuo2ouebe2vfiucvi2ev'
    app.run(host='0.0.0.0', debug=True)