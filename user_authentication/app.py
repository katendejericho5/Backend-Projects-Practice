from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user


# Create a flask application
app = Flask(__name__)

# Tells flask-sqlalchemy what database to connect to
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
# Enter a secret key
app.config["SECRET_KEY"] = "secret_key"
# Initialize flask-sqlalchemy extension
db = SQLAlchemy()

# LoginManager is needed for our application 
# to be able to log in and out users
login_manager = LoginManager()
login_manager.init_app(app)


# models 
# Create user model
class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(250), unique=True,
						nullable=False)
	password = db.Column(db.String(250),
						nullable=False)


# Initialize app with extension
db.init_app(app)
# Create database within app context

with app.app_context():
	db.create_all()

# Creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)

@app.route('/register', methods=["GET", "POST"])
def register():
# If the user made a POST request, create a new user
	if request.method == "POST":
		user = Users(username=request.form.get("username"),
					password=request.form.get("password"))
		# Add the user to the database
		db.session.add(user)
		# Commit the changes made
		db.session.commit()
		# Once user account created, redirect them
		# to login route (created later on)
		return redirect(url_for("login"))
	# Renders sign_up template if user made a GET request
	return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
	# If a post request was made, find the user by 
	# filtering for the username
	if request.method == "POST":
		user = Users.query.filter_by(
			username=request.form.get("username")).first()
		# Check if the password entered is the 
		# same as the user's password
		if user.password == request.form.get("password"):
			# Use the login_user method to log in the user
			login_user(user)
			return redirect(url_for("home"))
		# Redirect the user back to the home
		# (we'll create the home route in a moment)
	return render_template("login.html")

@app.route("/")
def home():
	# Render home.html on "/" route
	return render_template("home.html")

if __name__ == "__main__":
    app.run(
        debug=True,
            )