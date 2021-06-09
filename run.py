from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
from AzureDB import AzureDB
from datetime import datetime
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google
import secrets
import os

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'


# GITHUB AUTH
# Local settings
# github_blueprint = make_github_blueprint(client_id="86ce28230871d17590da",
#                                          client_secret="7ba727859885e9b8a2ee0ff1dcf80004298a40ee")

# github_blueprint = make_github_blueprint(client_id="9ef79816b268f73f3416",
#                                          client_secret="cd7425506758680d65db051fe070c6e3f9ab1be5")
# app.register_blueprint(github_blueprint, url_prefix='/login')


# @app.route('/')
# def github_login():
#     if not github.authorized:
#         return redirect(url_for('github.login'))
#     else:
#         account_info = github.get('/user')
#     if account_info.ok:
#         return render_template('index.html', title='Home')
#     return '<h1>Request failed!</h1>'


# GOOGLE AUTH

# app.config["GOOGLE_OAUTH_CLIENT_ID"] = "821397628860-f99glj2t8f9leglgeubqn1l1410ho2m0.apps.googleusercontent.com"
# app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = "EfnLGwN51KVfaKfrHLJHJLMy"
# google_bp = make_google_blueprint(scope=["email", "profile"])
# app.register_blueprint(google_bp, url_prefix="/login")
#
#
# @app.route("/")
# def index():
#     if not google.authorized:
#         return redirect(url_for("google.login"))
#     resp = google.get("/oauth2/v1/userinfo")
#     assert resp.ok, resp.text
#     return render_template('index.html', title='Home')


@app.route('/home')
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
