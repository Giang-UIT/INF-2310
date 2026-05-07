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
REDIRECT_URI = "https://gng000.inf2310.net/getAToken"

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
    # TODO: Use the auth object to log in.
    res = auth.log_in(SCOPES, REDIRECT_URI)
    
    #print(f"this is from login: {res}")
    response = res

    return render_template("login.html", **response)

@app.route(REDIRECT_PATH)
def auth_response():
    # TODO: Use the flask request object and auth object to complete the authentication.
    
    res = auth.complete_log_in(request.args)
    #print(f"this is from auth response: {res}")
    
    if res.get("error"):
        return render_template("auth_error.html", result = res)
    
    return redirect(url_for("index", _external = False))

@app.route("/logout")
def logout():
    # TODO: Use the auth object to log out and redirect to the home page
    #res = auth.log_out(url_for("index"))
    #print(f"this is from logout: {res}")
    
    return redirect(auth.log_out(url_for("index", _external = True)))


@app.route("/")
def index():
    # TODO: use the auth object to get the profile of the logged in user.
    res = auth.get_user()
    
    print(f"from index: {res}")

    return render_template('index.html', user=res)


@app.route("/profile", methods=["GET"])
def get_profile():

    # TODO: Check that the user is loggen in and add credentials to the http request.
    res = auth.get_token_for_user(SCOPES)
    
    if not res.get("access_token"): 
        logout()
        return index()
    
    result = requests.get(
        'https://graph.microsoft.com/v1.0/me', 
        headers={'Authorization': 'Bearer' + res["access_token"]}
    )
    
    print(result)

    return render_template('profile.html', user=result.json(), result=None)

@app.route("/profile", methods=["POST"])
def post_profile():
    # TODO: check that the user is logged in and add credentials to the http request.
    
    res = auth.get_token_for_user(SCOPES)

    if not res.get("access_token"): 
        logout()
        return index()
    print(f"token: {res}")
    
    print(f"request form {request.form.to_dict()}")
    
    result = requests.patch(
        'https://graph.microsoft.com/v1.0/users/' + request.form["id"],
        headers={'Authorization': 'Bearer' + res["access_token"]},
        json=request.form.to_dict(),
    )
    
    

    # TODO: add credentials to the http request.
    profile = requests.get(
        'https://graph.microsoft.com/v1.0/me',
        headers={'Authorization': 'Bearer' + res["access_token"]}
    )
    
    print(f"response: {result}")
    return render_template('profile.html',
                           user=profile.json(),
                           result=result)


@app.route("/users")
def get_users():

    # TODO: Check that user is logged in and add credentials to the request.
    
    res = auth.get_token_for_user(SCOPES)
    
    if not res.get("access_token"): 
        logout()
        return index()

    result = requests.get(
        'https://graph.microsoft.com/v1.0/users',
        headers={'Authorization': 'Bearer' + res["access_token"]}
    )
    
    #print(f"from get_users: {result}")
    
    return render_template('users.html', result=result.json())


if __name__ == "__main__":
    app.run()
