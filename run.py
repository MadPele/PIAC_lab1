from flask import Flask
from flask import render_template
from flask import request
from AzureDB import AzureDB
from datetime import datetime


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


@app.route('/guestbook')
def guestbook():
    with AzureDB() as a:
        data = a.azureGetData()
        return render_template("guestbook.html", data=data, title='GuestBook')


@app.route('/addcomment')
def addcomment():
    return render_template("addcomment.html", title='Add Comment')


@app.route('/thankyou', methods=['POST'])
def thankyou():
    if request.method == 'POST':
        name = request.form['name']
        comment = request.form['comment']
        date = str(datetime.now())
        with AzureDB() as a:
            a.azureAddData(name, comment, date[:19])
    return render_template('thankyou.html', title='Dziękuje', metod='POST')


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    index = request.form['id']
    with AzureDB() as a:
        a.azureDeleteData(index)
        return render_template('thankyou.html', title='Dziękuje', metod='DELETE')


@app.route('/edit', methods=['POST', 'GET'])
def edit():
    index = request.form['id']
    with AzureDB() as a:
        data = a.azureGetOneData(index)
        return render_template('editcomment.html', title='Edytowanie', nick=data[1], comment=data[2], id=data[0])


@app.route('/update', methods=['POST', 'GET'])
def update():
    index = request.form['id']
    name = request.form['name']
    text = request.form['text']
    with AzureDB() as a:
        a.azureUpdateData(index, name, text)
        return render_template('thankyou.html', title='Dziękuje', metod='UPDATE')


@app.errorhandler(404)
def not_found_error():
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
