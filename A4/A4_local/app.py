import identity.web
import requests
import os
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session

# The following variables are required for the app to run.

# TODO: Use the Azure portal to register your application and generate client id and secret credentials.
CLIENT_ID = "75f89cdd-29b6-408a-9d29-87a63d3b3bcf"
CLIENT_SECRET = "P5u8Q~PUCjgRC8qNJoEmwacQ3~lniPYRYI7WXdt~"  

# TODO: Figure out your authentication authority id.
AUTHORITY = "https://login.microsoftonline.com/3636fa81-951c-4f09-9883-e464c784f7d1"

# TODO: generate a secret. Used by flask session for protecting cookies.
SESSION_SECRET = "f7724a5caff0906fc2fa42aeb4155ceab1ed5b5bd19114251d1cc529c9d08a40"

# TODO: Figure out what scopes you need to use
SCOPES = ["User.Read", "User.ReadWrite","User.ReadWrite.All"]

# TODO: Figure out the URO where Azure will redirect to after authentication. After deployment, this should
#  be on your server. The URI must match one you have configured in your application registration.
REDIRECT_URI = "http://localhost:5000/getAToken"

REDIRECT_PATH = "/getAToken"

app = Flask(__name__)

app.config['SECRET_KEY'] = SESSION_SECRET
app.config['SESSION_TYPE'] = 'filesystem'
app.config['TESTING'] = True
app.config['DEBUG'] = True
Session(app)

# The auth object provide methods for interacting with the Microsoft OpenID service.
auth = identity.web.Auth(session=session,
                         authority=AUTHORITY,
                         client_id=CLIENT_ID,
                         client_credential=CLIENT_SECRET)

@app.route("/login")
def login():
    res = auth.log_in(SCOPES, REDIRECT_URI)
    
    response = res
    
    if not response:
        return index()

    return render_template("login.html", **response)

@app.route(REDIRECT_PATH)
def auth_response():
    
    res = auth.complete_log_in(request.args)
    
    if res.get("error"):
        return render_template("auth_error.html", result = res)
    
    return redirect(url_for("index", _external = False))

@app.route("/logout")
def logout():
    
    redirect(auth.log_out(url_for("index", _external = True)))
    
    return index() 


@app.route("/")
def index():
    res = auth.get_user()
        
    return render_template('index.html', user=res)


@app.route("/profile", methods=["GET"])
def get_profile():
    res = auth.get_token_for_user(SCOPES)
    
    if not res.get("access_token"): 
        logout()
        return render_template("profile_error.html", result = res)
    
    result = requests.get(
        'https://graph.microsoft.com/v1.0/me', 
        headers={'Authorization': 'Bearer' + res["access_token"]}
    )

    return render_template('profile.html', user=result.json(), result=None)

@app.route("/profile", methods=["POST"])
def post_profile():
    
    res = auth.get_token_for_user(SCOPES)

    if not res.get("access_token"): 
        logout()
        return render_template("post_error.html", result = res)

    result = requests.patch(
        'https://graph.microsoft.com/v1.0/users/' + request.form["id"],
        headers={'Authorization': 'Bearer' + res["access_token"]},
        json=request.form.to_dict(),
    )
    
    profile = requests.get(
        'https://graph.microsoft.com/v1.0/me',
        headers={'Authorization': 'Bearer' + res["access_token"]}
    )
    
    return render_template('profile.html',
                           user=profile.json(),
                           result=result)


@app.route("/users")
def get_users():

    res = auth.get_token_for_user(SCOPES)
    
    if not res.get("access_token"): 
        logout()
        return render_template("get_error.html", result = res)

    result = requests.get(
        'https://graph.microsoft.com/v1.0/users',
        headers={'Authorization': 'Bearer' + res["access_token"]}
    )
    
    
    return render_template('users.html', result=result.json())


if __name__ == "__main__":
    app.run()
