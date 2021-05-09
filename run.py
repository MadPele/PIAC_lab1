from flask import Flask
from flask import request
from flask import render_template
from flask import abort, redirect, url_for, make_response


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'),


if __name__=='__main__':
    app.run(debug=True)