from flask import Flask, render_template, url_for
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = 'dijfonoon32'

app.config['SERVER_NAME'] = 'localhost:5000'
oauth = OAuth(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/google/')
def google():
    GOOGLE_CLIENT_ID = os.environ.get('677233232305-mvh4499eksbl8uoa91o5pejv02vsbkvr.apps.googleusercontent.com')
    GOOGLE_CLIENT_SECRET = os.environ.get('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')
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google', 
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope':'openid email profile'
        }
    )

    redirect_uri = url_for('google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    print(" Google User", user)
    return redirect('/')

@app.route('/x/')
def x():
    X_CLIENT_ID = os.environ.get('RmRsZklOREhfVzk5bHNXNFZwa3Y6MTpjaQ')
    X_CLIENT_SECRET = os.environ.get('HRSEywLvx07uzk2Pfqa0V9zYc667f40rAE5jrwtxPU9rzAK')
    oauth.register(
        name='x',
        client_id=X_CLIENT_ID, 
        client_secret=X_CLIENT_SECRET,
        request_token_url='https://api.twitter.com/oauth/request_token',
        request_token_params=None, 
        access_token_url='https://api.twitter.com/oauth/access_token',
        access_token_params=None, 
        authorize_url='https://api.twitter.com/oauth/authenticate',
        authorize_params=None, 
        api_base_url='https://api.twitter.com/1.1/',
        client_kwargs=None,
    )
    redirect_url = url_for('x_auth', _external=True)
    return oauth.x.authorize_redirect(redirect_url)

@app.route('/x/auth/')
def x_auth():
    token = oauth.x.authorize_access_token()
    resp = oauth.x.get('account/verify_credentials.json')
    profile = resp.json()
    print(" X User ", profile)
    return redirect('/')

@app.route('/facebook/')
def facebook():
    FACEBOOK_CLIENT_ID = os.environ.get('782100590609324')
    FACEBOOK_CLIENT_SECRET = os.environ.get('7951ba9be5d77bc12d376891fff87749')
    oauth.register(
        name='facebook', 
        client_id=FACEBOOK_CLIENT_ID,
        client_secret=FACEBOOK_CLIENT_SECRET,
        access_token_url='https://graph.facebook.com/oauth/access_token',
        access_token_params=None, 
        authorize_url='https://www.facebook.com/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/',
        client_kwargs={'scope': 'email'},
    )
    redirect_url=url_for('facebook_auth', _external=True)
    return oauth.facebook.authorize_redirect(redirect_url)

@app.route('/facebook/auth/')
def facebook_auth():
    token = oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get(
        'https://graph.facebook.com/me?fields=id,name,email,picture{url}')
    profile = resp.json()
    print("Facebook User", profile)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)