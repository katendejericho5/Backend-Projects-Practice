from flask import Flask, request, jsonify, make_response, render_template, session, flash
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KEEP_IT_A_SECRET'

@app.route('/public')
def public():
 return 'Anyone can access this'

if __name__ == '__main__':
 app.run(debug=True)