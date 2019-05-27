"""
File Path: application/modules/auth/views.py
Description: Auth routes/paths for App - Define auth/login paths/routes
Copyright (c) 2019. This Application has been developed by OR73.
"""
import datetime
import httplib2
import json
import random
import requests
import string

from flask import Blueprint, flash, jsonify, make_response, redirect, render_template, request, session, url_for
from flask_login import login_required, login_user, logout_user
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
# ------------------------ HTTP Authorization
from flask_httpauth import HTTPBasicAuth  # python 3
from oauth2client.contrib.flask_util import UserOAuth2

from instance.config import Config

# Methods
from auth.methods import AuthMethod
from user.methods import UserMethod
# Models
from .models import Auth
from user.models import User

from setup import db

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """ Login 'local' user """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    # Login code
    if request.method == 'POST':
        print('login method - POST - ', request.method)
        # Retrieve data
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = UserMethod.get_user(email)
        """# Validate if the auth exists """

        if not user or not user.validate_password(password):
            """ Check if user actually exists take the auth supplied password, hash it,
                   and compare it to the hashed password in the database if not auth or
                   not check_password_hash(auth.password, password):"""
            print('User does not exist...')
            flash('Please check your login details and try again!')
            return redirect(url_for('auth_bp.login'))  # if auth does not exist or password is wrong, reload the page

        user.set_session_token()
        """ Generate new session_token for current_user """
        db.session.merge(user)
        """ Update session_token to current_user """
        db.session.commit()
        """ Commit User object modifications """
        session_token = user.get_session_token()
        """ Retrieve the session_token of current_user"""
        # user.generate_auth_token(600)
        # """ Create session Token """
        # if the above check passes, then the User has the right credentials
        login_user(user, remember=remember)
        """ Add user to session environment """

        update_session(access_token=session_token,
                       authenticated=True,
                       email=email,
                       first_name=user.get_first_name(),
                       last_name=user.get_last_name(),
                       password=password,
                       picture='',
                       profile=False,
                       provider='local',
                       session_id=state,
                       session_token=session_token,
                       state=state,
                       username=user.get_username())
        """ Store data into session """

        # auth = Auth(user_id=user.id)
        auth = AuthMethod.create_auth(user_id=user.id)
        """ Create Auth & Store login_time """
        if not auth:
            flash('Something was wrong, and session could not be initiated... try again')
        return redirect(url_for('catalog_bp.index'))
    elif request.method == 'GET':
        print('login method - GET - ', request.method)
        return render_template('auth/login.html',
                               state=state)


def mk_response(message, code, c_type):
    """ Make response message """
    response = make_response(json.dumps(message), code)
    response.headers['Content-type'] = c_type
    return response


def update_session(access_token, authenticated, email, first_name, last_name, password, picture, profile, provider,
                   session_id, session_token, state, username):
    """ Store all provided data in current session"""
    session['access_token'] = access_token
    session['authenticated'] = authenticated
    session['email'] = email
    session['first_name'] = first_name
    session['last_name'] = last_name
    session['password'] = password
    session['picture'] = picture
    session['profile'] = profile
    session['provider'] = provider
    session['session_id'] = session_id
    session['session_token'] = session_token
    session['state'] = state
    session['username'] = username


@auth_bp.route('/login/<provider>', methods=['POST'])
def login_provider(provider):
    """This is only for Facebook and Gmail login/signup"""
    global auth_code, credentials, data, picture_aux, session_id_aux, token, url
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    print('-------------------- login_provider: ', request.method)
    if request.method == 'POST':
        # Validate session STATE
        print('login <provider> - session[state]: ', session['state'])
        print('login <provider> - request.args.get(state): ', request.args.get('state'))
        if request.args.get('state') != session['state']:
            print('Session STATE invalid')
            return mk_response('Invalid state parameter', 400, 'application/json')
        print('------------------ %s Login ------------------' % provider)
        print('STEP 1. Parse auth')
        if provider == 'google':
            auth_code = request.data
        elif provider == 'facebook':
            auth_code = request.data.decode('utf-8')

        print('STEP 2. Exchange for a Token')
        if provider == 'google':
            try:
                # upgrade the authorization code into a credential object
                oauth_flow = flow_from_clientsecrets('application/secrets/client_secrets_gmail.json', scope='')
                oauth_flow.redirect_uri = 'postmessage'
                credentials = oauth_flow.step2_exchange(auth_code)
            except FlowExchangeError:
                return mk_response('Failed to upgrade the authorization code', 401, 'application/json')
            token = credentials.access_token
            url = (Config.google_url_token + token)
        elif provider == 'facebook':
            url = Config.facebook_url_client_id + Config.FACEBOOK_APP_ID + \
                  Config.facebook_url_client_secret + Config.FACEBOOK_SECRET + \
                  Config.facebook_url_fb_exchange_token + auth_code

        h = httplib2.Http()
        result = h.request(url, 'GET')[1]

        if provider == 'google':
            result = json.loads(result)
            if result.get('error') is not None:
                return mk_response(result.get('error'), 500, 'application/json')
            gmail_id = credentials.id_token['sub']
            if result['user_id'] != gmail_id:
                return mk_response('Token doesn\'t match given user_id', 401, 'application/json')
            # Verify that the access token is valid for this app
            if result['issued_to'] != Config.GMAIL_CLIENT_ID:
                return mk_response('Token doesn\'t match the app', 401, 'application/json')
            stored_access_token = session.get('access_token')
            stored_gmail_id = session.get('gmail_id')
            if stored_access_token is not None and gmail_id == stored_gmail_id:
                return mk_response('Current user is already connected', 200, 'application/json')
            params = {'access_token': credentials.access_token, 'alt': 'json'}
            answer = requests.get(Config.facebook_url_userinfo, params=params)
            data = answer.json()
            token = credentials.access_token
            picture_aux = data['picture']
            session_id_aux = gmail_id
        elif provider == 'facebook':
            result = result.decode('utf-8')
            token = result.split(',')[0].split(':')[1].replace('"', '')
            print('facebook - token: ', token)
            url = (Config.facebook_url_token1 + token + Config.facebook_url_token2)
            print('facebook - url token: ', url)
            h = httplib2.Http()
            result = h.request(url, 'GET')[1]
            print('facebook - result token: ', result)
            data = json.loads(result)
            print('facebook - data: ', data)
            # Get user picture
            url = Config.facebook_url_picture1 + token + Config.facebook_url_picture2
            print('facebook - url picture: ', url)
            h = httplib2.Http()
            result = h.request(url, 'GET')[1]
            print('facebook - result image: ', result)
            data_picture = json.loads(result)
            print('facebook - data picture: ', data_picture)
            picture_aux = data_picture['data']['url']
            session_id_aux = data['id']

        print('STEP 3. Store data in session')
        update_session(access_token=token,
                       authenticated=True,
                       email=data['email'],
                       first_name='',
                       last_name='',
                       password=Config.DEFAULT_PWD,
                       picture=picture_aux,
                       profile=False,
                       provider=provider,
                       session_id=session_id_aux,
                       session_token=None,
                       state=state,
                       username=data['name'])

        print('STEP 3. Validate if user exists in DB')
        # user = user_bp.get_user(session['email'])

        # Validate if the auth exists
        user = UserMethod.get_user(data['email'])  # User.query.filter_by(email=data['email']).first()

        if not user:
            print('User does not exist... creating new user...')
            print('session: ', session)
            user_id = UserMethod.create_user(session)
            print('user_id: ', user_id)
            user = UserMethod.get_user_info_id(user_id)
            print('user: ', user)

        # print('STEP 5. Generate Token')
        # session_token = user.generate_auth_token(600)

        # if the above check passes, then the auth has the right credentials
        login_user(user, remember=True)

        print('STEP 6. Store session_token data in session')

        """ Store data into session """
        session['session_token'] = user.get_session_token() # session_token

        auth = AuthMethod.create_auth(user_id=user.id)
        """ Create Auth & Store login_time """

        # if the above check passes, then the User has the right credentials
        login_user(user, remember=True)
        """ Add user to session environment """
        if not auth:
            flash('Something was wrong, and session could not be initiated... try again')

        # return jsonify({'token': session_token.decode('ascii')})
        return jsonify({'token': session['session_token'].decode('ascii')})


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    print('request.method: ', request.method)
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    session['state'] = state
    if request.method == 'POST':
        # code to validate and add auth to database
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        authenticated = False
        picture = ''
        profile = 'user'
        provider = 'local'

        user = UserMethod.get_user(email)  # if this returns a auth, then the email already exists in DB

        if user:  # if a auth is found, then redirect back to signup page so auth can try again
            flash('Email address already exists')
            return redirect(url_for('auth_bp.signup'))

        # create a new auth with the form data.  Hash the password so plaintext version isn't saved
        new_user = User(authenticated=authenticated,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        password=password,
                        picture=picture,
                        profile=profile,
                        provider=provider,
                        session_token=None,
                        username=username)

        # Add new auth to DB
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth_bp.login'))
    print('signup - session{state]: ', session['state'])
    return render_template('auth/signup.html',
                           facebook_app_id=Config.FACEBOOK_APP_ID,
                           gmail_client_id=Config.GMAIL_CLIENT_ID,
                           state=state)


# DISCONNECT - Revoke a current user's token and reset their session
@auth_bp.route('/fb_disconnect')
def fb_disconnect():
    global url
    facebook_id = session['session_id']
    # The access token must me included to successfully logout
    access_token = session['access_token']
    url = Config.facebook_url_logout1 + facebook_id + Config.facebook_url_logout2 + access_token
    # url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out " + str(result)


# DISCONNECT - Revoke a current user's token and reset their session
@auth_bp.route('/g_disconnect')
def g_disconnect():
    global url
    # Only disconnect a connected user.
    access_token = session.get('access_token')
    if access_token is None:
        response = mk_response('Current user not connected.', 401, 'application/json')
        return response
    url = Config.google_url_logout + access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@auth_bp.route('/logout')
@login_required
def logout():
    print('---------------------- Auth - logout')
    logout_user()
    """ logout current user from session """

    if 'username' in session:
        print('user in session')
        user_id = UserMethod.get_user_id_session_token(session['session_token'])
        """ Update logout_time of current user """

        auth = Auth.query.filter_by(user_id=user_id).order_by(Auth.login_time.desc()).first()
        """ Load current user session object to update """

        auth.set_logout_time()  # logout_time = datetime.datetime.now()
        """ Update current user session logout time"""
        db.session.merge(auth)
        """ Merge updated Auth object with object in DB """
        db.session.commit()
        """ Commit Update operation """

        # Validate provider
        if session['provider'] == 'google':
            print('-------------- LOGOUT Gmail')
            g_disconnect()
            """ Disconnect function for Gmail session """

        if session['provider'] == 'facebook':
            print('-------------- LOGOUT Facebook')
            fb_disconnect()
            """ Disconnect facebook_id for Facebook session """

        """ Delete all data from session """
        del session['access_token']
        del session['email']
        del session['password']
        del session['picture']
        del session['profile']
        del session['provider']
        del session['session_id']
        del session['session_token']
        del session['username']

        session.modified = True
        # oauth2.storage.delete()
    return redirect(url_for('catalog_bp.index'))
