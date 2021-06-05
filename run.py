from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', title='Home')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html', title='Gallery')


@app.route('/about')
def about():
    return render_template('about.html', title='About Me')


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html', title='Thank You!')


@app.errorhandler(404)
def not_found_error():
    return render_template('404.html')


if __name__=='__main__':
    app.run(debug=True)