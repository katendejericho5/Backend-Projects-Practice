import jwt
from flask import Flask, request, jsonify, make_response
import datetime

app = Flask(__name__)

app.config['secret_key'] = "this is secret"


def token_required(f):
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'error': 'token is missing'}), 403
        try:
            jwt.decode(token, app.config['secret_key'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'error': 'token is invalid'}), 403
        return f(*args, **kwargs)
    return decorated


@app.route("/login")
def login():
    auth = request.authorization
    if auth and auth.password == "password":
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(seconds=10)}, app.config['secret_key'], algorithm="HS256")
        
        # Convert token to string if it's in bytes
        token_str = token if isinstance(token, str) else token.decode('utf-8')
        
        return f'<a href="http://localhost:5001/access?token={token_str}">Private link</a>'
    return make_response('Could not Verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route("/access")
@token_required
def access():
    return jsonify({'message': 'valid jwt token'})


if __name__ == "__main__":
    app.run(port=5002)
