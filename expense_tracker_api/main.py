from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jericho_secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Initialize Limiter without passing the app
limiter = Limiter(key_func=get_remote_address)

# Attach Limiter to the app
limiter.init_app(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    expenses = db.relationship('Expense', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Authentication routes
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already registered"}), 400
    user = User(name=data['name'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 201

@auth.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200
    return jsonify({"message": "Invalid email or password"}), 401

@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({"access_token": access_token}), 200

# Expense routes
expenses = Blueprint('expenses', __name__)

@expenses.route('', methods=['POST'])
@jwt_required()
def add_expense():
    current_user = get_jwt_identity()
    data = request.get_json()
    new_expense = Expense(
        amount=data['amount'],
        description=data['description'],
        category=data['category'],
        date=datetime.fromisoformat(data['date']),
        user_id=current_user
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({"message": "Expense added successfully"}), 201

@expenses.route('', methods=['GET'])
@jwt_required()
def get_expenses():
    current_user = get_jwt_identity()
    filter_type = request.args.get('filter', 'all')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Expense.query.filter_by(user_id=current_user)
    
    if filter_type == 'week':
        query = query.filter(Expense.date >= datetime.utcnow() - timedelta(days=7))
    elif filter_type == 'month':
        query = query.filter(Expense.date >= datetime.utcnow() - timedelta(days=30))
    elif filter_type == 'three_months':
        query = query.filter(Expense.date >= datetime.utcnow() - timedelta(days=90))
    elif filter_type == 'custom':
        if start_date and end_date:
            query = query.filter(Expense.date.between(start_date, end_date))
    
    expenses = query.all()
    return jsonify([{
        'id': e.id,
        'amount': e.amount,
        'description': e.description,
        'category': e.category,
        'date': e.date.isoformat()
    } for e in expenses]), 200

@expenses.route('/<int:expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    current_user = get_jwt_identity()
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user).first()
    if not expense:
        return jsonify({"message": "Expense not found"}), 404
    
    data = request.get_json()
    expense.amount = data.get('amount', expense.amount)
    expense.description = data.get('description', expense.description)
    expense.category = data.get('category', expense.category)
    expense.date = datetime.fromisoformat(data.get('date', expense.date.isoformat()))
    
    db.session.commit()
    return jsonify({"message": "Expense updated successfully"}), 200

@expenses.route('/<int:expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    current_user = get_jwt_identity()
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user).first()
    if not expense:
        return jsonify({"message": "Expense not found"}), 404
    
    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Expense deleted successfully"}), 200

# Register blueprints
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(expenses, url_prefix='/expenses')

if __name__ == '__main__':
    app.run(debug=True)
