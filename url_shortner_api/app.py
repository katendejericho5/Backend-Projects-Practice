from flask import Flask, request, jsonify, redirect, abort
from flask_sqlalchemy import SQLAlchemy
import string
import random
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model for storing URLs
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(6), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    access_count = db.Column(db.Integer, default=0)

# Helper function to generate a short code
def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# Endpoint to create a new short URL
@app.route('/shorten', methods=['POST'])
def create_short_url():
    data = request.get_json()
    original_url = data.get('url')
    if not original_url:
        return jsonify({"error": "Invalid request"}), 400

    short_code = generate_short_code()
    while URL.query.filter_by(short_code=short_code).first():
        short_code = generate_short_code()

    new_url = URL(original_url=original_url, short_code=short_code)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({
        "id": new_url.id,
        "url": new_url.original_url,
        "shortCode": new_url.short_code,
        "createdAt": new_url.created_at.isoformat(),
        "updatedAt": new_url.updated_at.isoformat()
    }), 201

# Endpoint to retrieve the original URL
@app.route('/shorten/<string:short_code>', methods=['GET'])
def retrieve_original_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if not url:
        return jsonify({"error": "URL not found"}), 404

    url.access_count += 1
    db.session.commit()

    return jsonify({
        "id": url.id,
        "url": url.original_url,
        "shortCode": url.short_code,
        "createdAt": url.created_at.isoformat(),
        "updatedAt": url.updated_at.isoformat(),
        "accessCount": url.access_count
    })

# Endpoint to update an existing short URL
@app.route('/shorten/<string:short_code>', methods=['PUT'])
def update_short_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if not url:
        return jsonify({"error": "URL not found"}), 404

    data = request.get_json()
    new_url = data.get('url')
    if not new_url:
        return jsonify({"error": "Invalid request"}), 400

    url.original_url = new_url
    url.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "id": url.id,
        "url": url.original_url,
        "shortCode": url.short_code,
        "createdAt": url.created_at.isoformat(),
        "updatedAt": url.updated_at.isoformat()
    })

# Endpoint to delete an existing short URL
@app.route('/shorten/<string:short_code>', methods=['DELETE'])
def delete_short_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if not url:
        return jsonify({"error": "URL not found"}), 404

    db.session.delete(url)
    db.session.commit()

    return '', 204

# Endpoint to get statistics of a short URL
@app.route('/shorten/<string:short_code>/stats', methods=['GET'])
def get_url_stats(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if not url:
        return jsonify({"error": "URL not found"}), 404

    return jsonify({
        "id": url.id,
        "url": url.original_url,
        "shortCode": url.short_code,
        "createdAt": url.created_at.isoformat(),
        "updatedAt": url.updated_at.isoformat(),
        "accessCount": url.access_count
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
