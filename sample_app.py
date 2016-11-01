from flask import Flask
from flask import Markup
from flask import redirect
from flask import request
from flask import jsonify
import json

from weixin.client import WeixinAPI
from weixin.oauth2 import OAuth2AuthExchangeError

app = Flask(__name__)

def Initialization():
	global APP_ID, APP_SECRET, REDIRECT_URI
	REDIRECT_URI = 'http://localhost.com/authorization'
	FILE = open("tencent_open_token.json")
	rawdata = FILE.read()
	json_data = json.loads(rawdata)
	APPID = json_data["app_id"]
	APP_SECRET = json_data["app_secret"]
	FILE.close()
	return 0

@app.route("/authorization")
def authorization():
	global APP_ID, APP_SECRET, REDIRECT_URI
    code = request.args.get('code')
    api = WeixinAPI(appid=APP_ID,REDIRECT_URI
                    app_secret=APP_SECRET,
                    redirect_uri=REDIRECT_URI)
    auth_info = api.exchange_code_for_access_token(code=code)
    api = WeixinAPI(access_token=auth_info['access_token'])
    resp = api.user(openid=auth_info['openid'])
    return jsonify(resp)


@app.route("/login")
def login():
	global APP_ID, APP_SECRET, REDIRECT_URI
    api = WeixinAPI(appid=APP_ID,
                    app_secret=APP_SECRET,
                    redirect_uri=REDIRECT_URI)
    redirect_uri = api.get_authorize_login_url(scope=("snsapi_base",))
    return redirect(redirect_uri)


@app.route("/")
def hello():
    return Markup('<a href="%s">weixin login!</a>') % '/login'

if __name__ == "__main__":
	Initialization()
    app.run(host='0.0.0.0',debug=True)
