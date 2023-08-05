from .SecurityLayer import SecurityLayer
from .AccessControl import *
from .Error import *
from dtwentyORM import Metadata
from Communications.Communications import Communications
from flask import request, redirect, url_for
import json
import datetime
from .default import crypt as D20_SL_CRYPTOKEY

def sso_password_reset(**kwargs):
    jr = kwargs.get('jr')
    if not 'token' in jr or not 'password' in jr:
        return SSOInvalidRequestError().make_error()
    if os.environ.get('D20_SL_CONF') != None:
        env = json.loads(os.environ.get('D20_SL_CONF'))
        crypt = env.get('D20_SL_CRYPTOKEY').encode()
    else:
        crypt = D20_SL_CRYPTOKEY
    f = Fernet(crypt)
    try:
        val, userid, token_id = f.decrypt(bytes(jr['token'], 'utf-8')).decode().split('.')
    except:
        val = 'error'
    if val != 'passwordrec':
        return SSOInvalidTokenError().make_error()
    # TODO: destroying at first try generates non-second changes
    token = SecurityLayer.PasswordRecoveryToken('find', {'_key': token_id, 'userid': userid})
    print(token.to_dict())
    if token.get('status') != True:
        return SSOInvalidTokenError().make_error()
    access = SecurityLayer.UserAccess('update', {'_key': userid, 'password':jr.get('password')})
    print(access.to_dict())
    # Differenciate between no change and error
    # if access.get('status') != True:
    #     return UnexpectedError().make_error()
    utoken = SecurityLayer.UserToken('auth', {'username': userid, 'password':jr.get('password')})
    tokenid = utoken.get('_key')
    p = Metadata.Parameter('find', {'_key' : 'reset_password_redirect'})
    redir_uri = jr.get('redir_uri', p.get('value'))
    if os.environ.get('D20_SL_CONF') != None:
        env = json.loads(os.environ.get('D20_SL_CONF'))
        crypt = env.get('D20_SL_CRYPTOKEY').encode()
    else:
        crypt = D20_SL_CRYPTOKEY
    f = Fernet(crypt)
    refresh_token = f.encrypt(bytes(f'{tokenid}.{userid}', 'utf-8')).decode()
    access_token = f.encrypt(bytes(f'{userid}.{tokenid}', 'utf-8')).decode()
    oauth_params = f'acces_token={access_token}&refresh_token={refresh_token}'
    return jsonify({'res': True, 'redirect_uri': f'{redir_uri}?{oauth_params}'})
    
def oauth_sendpasswordrecovery(welcome = False):
    auth = api_back_auth(request, oauth=True)
    if auth.get('res') == False:
        return jsonify({'error': auth.get('err_desc')}), auth.get('err_code')
    atoken = auth.get('token')
    if atoken.get('oauth') != True or not 'auth' in atoken.get('actions'):
        return jsonify({'error': 'unauthorized_client'}), 401
    jr = request.get_json()
    m = Core.User('find', {'username': jr.get('username')})
    if m.get('status') != True:
        return jsonify("Member not found"), 404
    email_parameters = m.to_dict()
    userid = m.get('_key')
    rtoken = SecurityLayer.PasswordRecoveryToken('create', {'userid':m.get('_key')})
    tokenid = rtoken.get('_key')
    code = f'{userid}.{tokenid}'
    if os.environ.get('D20_SL_CONF') != None:
        env = json.loads(os.environ.get('D20_SL_CONF'))
        crypt = env.get('D20_SL_CRYPTOKEY').encode()
    else:
        crypt = D20_SL_CRYPTOKEY
    f = Fernet(crypt)
    token = f.encrypt(bytes(f'passwordrec.{code}', 'utf-8')).decode()
    p = Metadata.Parameter('find', {'_key' : 'oauth_passwordreset_url'})
    base_url = p.get('value')
    email_parameters['url'] = f'{base_url}?token={token}&client_id={atoken.get("_key")}'
    if 'back_uri' in jr:
        email_parameters['url'] = f'{email_parameters["url"]}&back_uri={jr.get("back_uri")}'
    email_type = 'password_recovery_email'
    if welcome == True:
        email_type = 'welcome_email'
        act_token = SecurityLayer.UserToken('create', {'userid':m.get('_key')})
        act_token.valid_thru = act_token.valid_thru + datetime.timedelta(minutes=60*24*5)
        act_token.update()
        act_tokenid = act_token.get('_key')
        act_code = f'{userid}.{act_tokenid}'
        if os.environ.get('D20_SL_CONF') != None:
            env = json.loads(os.environ.get('D20_SL_CONF'))
            crypt = env.get('D20_SL_CRYPTOKEY').encode()
        else:
            crypt = D20_SL_CRYPTOKEY
        f = Fernet(crypt)
        activation_token = f.encrypt(bytes(f'{act_code}', 'utf-8')).decode()
        p = Metadata.Parameter('find', {'_key' : 'oauth_account_activation_url'})
        base_url = p.get('value')
        email_parameters['url_2'] = f'{base_url}?token={activation_token}&client_id={atoken.get("_key")}&channel=email'
        if 'back_uri' in jr:
            email_parameters['url_2'] = f'{email_parameters["url_2"]}&back_uri={jr.get("back_uri")}'
        else:
            p = Metadata.Parameter('find', {'_key' : 'default_redir_url'})
            email_parameters['url_2'] = f'{email_parameters["url_2"]}&back_uri={p.get("value")}'
    email = Communications.Email('set', {'receiver': m.get('email'), 'type':email_type, 'params': email_parameters})
    res = email.send()
    if res.get('res') != True:
        return jsonify({'error': auth.get('err_desc')}), auth.get('err_code')
    return jsonify(res)
    
def oauth_passwordrecoverylink():
    auth = api_back_auth(request, oauth=True)
    if auth.get('res') == False:
        return jsonify({'error': auth.get('err_desc')}), auth.get('err_code')
    atoken = auth.get('token')
    if atoken.get('oauth') != True or not 'auth' in atoken.get('actions'):
        return jsonify({'error': 'unauthorized_client'}), 401
    jr = request.get_json()
    auth = user_back_auth(request, oauth=True)
    if auth.get('res') == False:
        return jsonify({'error': auth.get('err_desc')}), auth.get('err_code')
    utoken = auth.get('token')
    m = Core.User('find', {'username': utoken.get('userid')})
    if m.get('status') != True:
        return jsonify("Member not found"), 404
    userid = m.get('_key')
    rtoken = SecurityLayer.PasswordRecoveryToken('create', {'userid':m.get('_key')})
    tokenid = rtoken.get('_key')
    code = f'{userid}.{tokenid}'
    if os.environ.get('D20_SL_CONF') != None:
        env = json.loads(os.environ.get('D20_SL_CONF'))
        crypt = env.get('D20_SL_CRYPTOKEY').encode()
    else:
        crypt = D20_SL_CRYPTOKEY
    f = Fernet(crypt)
    token = f.encrypt(bytes(f'passwordrec.{code}', 'utf-8')).decode()
    p = Metadata.Parameter('find', {'_key' : 'oauth_passwordreset_url'})
    base_url = p.get('value')
    url = f'{base_url}?token={token}&client_id={jr.get("oauth_client")}'
    if 'back_uri' in jr:
        url = f'{url}&back_uri={jr.get("back_uri")}'
    return jsonify({'url': url })

def oauth_error():
    p = Metadata.Parameter('find', {'_key' : 'oauth_server_error_url'})
    url = p.get('value')
    return redirect(f"{url}?error={request.args.get('error', )}")

def oauth_getactiontoken():
    jr = request.get_json()
    auth = api_back_auth(request, permalink=True, oauth=True)
    if auth.get('res') == False:
        return jsonify({'error': auth.get('err_desc')}), auth.get('err_code')
    atoken = auth.get('token')
    if atoken.get('oauth') != True or not 'sso_to_api' in atoken.get('actions'):
        return jsonify({'error': 'unauthorized_client'}), 401 
    if jr['token_type'].upper() != 'USER':
        return jsonify({'atoken': atoken.get('_key')}) 
    auth = user_back_auth(request, oauth=True)
    if auth.get('res') == False:
        return jsonify({'error': auth.get('err_desc')}), auth.get('err_code')
    utoken = auth.get('token')
    m = Core.User('find', {'_key': utoken.get('userid'), 'username': utoken.get('userid')})
    if not m.get('status') or m.get('_key') != jr['user_id']:
        return jsonify("Member not found"), 404
    return jsonify({'atoken': atoken.get('_key'), 'utoken': utoken.get('_key')}) 

# def sso_getuserinfo(Core, **kwargs):
#     atoken = kwargs.get('token')
#     utoken = kwargs.get('user_token')
#     m = Core.User('find', {'_key': utoken.get('userid'), 'username': utoken.get('userid')})
#     if not m.get('status'):
#         return UserNotFoundError().make_error()
#     return jsonify(m.dict_by_scope(atoken.get('oauth_scopes')))

def sso_logout(**kwargs):
    utoken = kwargs.get('user_token')
    if not utoken.get('status') == True:
        return SSOInvalidUserTokenError().make_error()
    utoken.wipe()
    if not utoken.get('status') == True:
        return UnexpectedError().make_error()
    return jsonify({'res': True})

def oauth_auth():
    auth = api_back_auth(request, permalink=True, oauth=True)
    if auth.get('res') == False:
        if request.method == 'GET':
            redirect_url = url_for('oauth_error') + auth.get('err_params')
            return redirect(redirect_url)
        else:
            return jsonify({'error': auth.get('err_desc')}), auth.get('err_code')
    atoken = auth.get('token')
    if request.method == 'GET':
        redirect_url = request.args.get('redirect_uri', atoken.get('oauth_urls')[0])
        if not redirect_url in atoken.get('oauth_urls') and max([redirect_url.find(url) for url in atoken.get('oauth_urls')]) != 0:
            redirect_url = url_for('oauth_error') + '?error=invalid_redirect_uri'
            return redirect(redirect_url)
        if not 'sso' in atoken.get('actions'):
            redirect_url = redirect_url + '?error=unauthorized_client'
            return redirect(redirect_url)
        if request.args.get('scopes', '') != '':
            scopes = request.args.get('scopes', '').split(' ')
        else:
            scopes = atoken.get('oauth_scopes')
        for scope in scopes:
            if not scope in atoken.get('oauth_scopes'):
                scopes.pop(scopes.index(scope))
        if len(scopes) <= 0:
            redirect_url = redirect_url + '?error=invalid_scope'
            return redirect(redirect_url)
        mode = ''
        if request.args.get('response_type', '') == 'token':
            mode = '0'
        p = Metadata.Parameter('find', {'_key' : 'oauth_server_login_url'})
        url = p.get('value')
        if 'Register' in request.args:
            return redirect(f"{url}?client_id={atoken.get('_key')}&state={request.args.get('state', '')}&redirect_uri={redirect_url}&scopes={' '.join(scopes)}&mode={mode}&orig=oauth2&Register")
        return redirect(f"{url}?client_id={atoken.get('_key')}&state={request.args.get('state', '')}&redirect_uri={redirect_url}&scopes={' '.join(scopes)}&mode={mode}&orig=oauth2")
    if request.method == 'POST':
        jr = request.get_json()
        if atoken.get('oauth') != True or not 'sso' in atoken.get('actions'):
            return jsonify({'error': 'unauthorized_client'}), 401 
        if jr.get('grant_type','') == 'auth':
            state = jr.get('state')
            redirect_url = jr.get('redirect_uri')
            if not redirect_url in atoken.get('oauth_urls') and max([redirect_url.find(url) for url in atoken.get('oauth_urls')]) != 0:
                return jsonify({'error': 'invalid_client', 'redirect_uri' : f'{redirect_url}?error=invalid_client'}), 401
            scopes = jr.get('scopes', [])
            if len(scopes) <= 0:
                return jsonify({'error': 'access_denied', 'redirect_uri' : f'{redirect_url}?error=access_denied'}), 403
            for scope in scopes:
                if not scope in atoken.get('oauth_scopes'):
                    scopes.pop(scopes.index(scope))
            if len(scopes) <= 0:
                return jsonify({'error': 'invalid_scope', 'redirect_uri' : f'{redirect_url}?error=invalid_scope'}), 403
            token_id = jr.get('token')
            userid = jr.get('userid')
            user = Core.User('find', {'username':userid})
            if user.get('status') != True:
                return jsonify({'error': 'unauthorized_client', 'redirect_uri' : f'{redirect_url}?error=unauthorized_client'}), 401
            userid = user.get('_key')
            token = SecurityLayer.UserToken('find', {'_key': token_id, 'userid': userid})
            if token.get('status') != True:
                return jsonify({'error': 'unauthorized_client', 'redirect_uri' : f'{redirect_url}?error=unauthorized_client'}), 401
            code = f'{userid}.{token_id}'
            if os.environ.get('D20_SL_CONF') != None:
                env = json.loads(os.environ.get('D20_SL_CONF'))
                crypt = env.get('D20_SL_CRYPTOKEY').encode()
            else:
                crypt = D20_SL_CRYPTOKEY
            f = Fernet(crypt)
            if jr.get('mode') == '0': # Implicit
                access_token = f.encrypt(bytes(code, 'utf-8')).decode()
                return jsonify({'redirect_uri' : f'{redirect_url}?state={state}&acces_token={access_token}' })
            else:
                token_challenge = f.encrypt(bytes(f'challenge.{code}', 'utf-8')).decode()
                return jsonify({'redirect_uri': f'{redirect_url}?state={state}&code={token_challenge}' })
        elif jr.get('grant_type', '') == 'code' or jr.get('grant_type', '') == 'authorization_code':
            if not 'code' in jr:
                return jsonify({'error': 'invalid_request'}), 401
            if os.environ.get('D20_SL_CONF') != None:
                env = json.loads(os.environ.get('D20_SL_CONF'))
                crypt = env.get('D20_SL_CRYPTOKEY').encode()
            else:
                crypt = D20_SL_CRYPTOKEY
            f = Fernet(crypt)
            try:
                val, userid, token_id = f.decrypt(bytes(jr['code'], 'utf-8')).decode().split('.')
            except:
                val = 'error'
            if val != 'challenge':
                return jsonify({'error': 'invalid_grant'}), 403
            token = SecurityLayer.UserToken('find', {'_key': token_id, 'userid': userid})
            if token.get('status') != True:
                return jsonify({'error': 'invalid_grant'}), 403
            rtoken = f.encrypt(bytes(f'{token_id}.{userid}', 'utf-8')).decode()
            code = f.encrypt(bytes(f'{userid}.{token_id}', 'utf-8')).decode()
            p = Metadata.Parameter('find', {'_key' : 'user_token_lifespawn'})
            lifespawn = p.get('value')
            return jsonify({
                "access_token":code,
                "token_type":"bearer",
                "expires_in":lifespawn*59,
                "refresh_token":rtoken,
            })
        elif jr.get('grant_type', '') == 'refresh_token':
            if not 'refresh_token' in jr:
                return jsonify({'error': 'invalid_request'}), 400
            if os.environ.get('D20_SL_CONF') != None:
                env = json.loads(os.environ.get('D20_SL_CONF'))
                crypt = env.get('D20_SL_CRYPTOKEY').encode()
            else:
                crypt = D20_SL_CRYPTOKEY
            f = Fernet(crypt)
            try:
                token_id, userid = f.decrypt(bytes(jr['refresh_token'], 'utf-8')).decode().split('.')
            except:
                return jsonify({'error': 'invalid_grant'}), 400
            token = SecurityLayer.UserToken('find', {'_key': token_id, 'userid': userid})
            if token.get('status') != True:
                return jsonify({'error': 'invalid_grant'}), 400
            code = f.encrypt(bytes(f'{userid}.{token_id}', 'utf-8')).decode()
            rtoken = f.encrypt(bytes(f'{token_id}.{userid}', 'utf-8')).decode()
            p = Metadata.Parameter('find', {'_key' : 'user_token_lifespawn'})
            lifespawn = p.get('value')
            return jsonify({
                "access_token":code,
                "token_type":"bearer",
                "expires_in":lifespawn*59,
                "refresh_token":rtoken,
            })
        else:
            return jsonify({'error': 'unsupported_grant_type'}), 401 