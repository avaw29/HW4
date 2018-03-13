# __authors__ = Jackie Cohen, Maulishree Pandey
# An application in Flask where you can log in and create user accounts to save Gif collections

# TODO 364: Check out the include giphy_api_key.py and follow instructions before proceeding to view functions.

# Import statements
import os
from giphy_api_key import api_key
from flask import Flask, render_template, session, redirect, request, url_for, flash

from flask_script import Manager, Shell

# New imports were needed for additional stuff for login
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField, SelectMultipleField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

# Imports for login management
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Configure base directory of app
basedir = os.path.abspath(os.path.dirname(__file__))

# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hardtoguessstring'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or "postgresql://localhost/HW4db" # TODO 364: Will need to create a database of this name. May also need to edit the database URL if your computer requires a password for you to run this.
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# App addition setups
manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# Login configurations setup
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app) # set up login manager

## Set up Shell context so it's easy to use the shell to debug
# Define function
def make_shell_context():
    return dict(app=app, db=db, User=User)

# Add shell context function use to manager
manager.add_command("shell", Shell(make_context=make_shell_context))


########################
######## Models ########
########################

## Association tables
# NOTE - (TODO 364: You may want to complete the models tasks below before returning to build the association tables! That will making doing this much easier.)

# TODO 364: Set up association Table between search terms and GIFs


# TODO 364: Set up association Table between GIFs and collections prepared by user



## User-related Models

# Special model for users to log in
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    #TODO 364: In order to complete the relationships between tables that are detailed below, you'll need to add fields to this User model. (Check out the TODOs for models below.)
    # Remember, the best way to do so is to add the fields, save your code, and then create and run a migration!

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

## DB load function
## Necessary for behind the scenes login manager that comes with flask_login capabilities! Won't run without this.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # returns User object or None

# Model to store gifs
class Gif(db.Model):
    pass
    # TODO 364: Add code for the Gif model such that it has the following fields:
    # id (Integer, primary key)
    # title (String up to 128 characters)
    # embedURL (String up to 256 characters)

    # TODO 364: Define a __repr__ method for the Gif model that shows the title and the URL of the gif

# Model to store a personal gif collection
class PersonalGifCollection(db.Model):
    pass
    # TODO 364: Add code for the PersonalGifCollection model such that it has the following fields:
    # id (Integer, primary key)
    # name (String, up to 255 characters)

    # This model should have a one-to-many relationship with the User model (one user, many personal collections of gifs -- say, "Happy Gif Collection" or "Sad Gif Collection")

    # This model should also have a many to many relationship with the Gif model.

class SearchTerm(db.Model):
    pass
    # TODO 364: Add code for the SearchTerm model such that it has the following fields:
    # id (Integer, primary key)
    # term (String, up to 32 characters, unique) -- You want to ensure the database cannot save non-unique searches
    # This model should have a many to many relationship with gifs

    # TODO 364: Define a __repr__ method for this model class that returns the term string


########################
######## Forms #########
########################

class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[Required(),Length(1,64),Email()])
    username = StringField('Username:',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password:',validators=[Required(),EqualTo('password2',message="Passwords must match")])
    password2 = PasswordField("Confirm Password:",validators=[Required()])
    submit = SubmitField('Register User')

    #Additional checking methods for the form
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

# TODO 364: The following forms for searching for gifs and creating collections are provided. You should examine them so you understand what data they pass along and can investigate as you build your view functions in TODOs below.
class GifSearchForm(FlaskForm):
    search = StringField("Enter a term to search GIFs", validators=[Required()])
    submit = SubmitField('Submit')

class CollectionCreateForm(FlaskForm):
    name = StringField('Collection Name',validators=[Required()])
    gif_picks = SelectMultipleField('GIFs to include')
    submit = SubmitField("Create Collection")

########################
### Helper functions ###
########################

def get_gif_by_id(id):
    """Should return gif object or None"""
    pass
    # TODO 364: This function should query for the gif with the input id and return either the corresponding gif, or the value None.

def get_or_create_gif(title, url):
    """Always returns a Gif instance"""
    pass
    # TODO 364: This function should get or create a Gif instance. Determining whether the gif already exists in the database should be based on its title.

def get_or_create_search_term(term):
    """Always returns a SearchTerm instance"""
    pass
    # TODO 364: This function should return the search term instance if it already exists.
    # If it does not exist in the database yet, this function should create a new SearchTerm instance.
    # This function should invoke the get_gifs_from_giphy function to get a list of gif data from Giphy.
    # It should iterate over that list from Giphy and invoke get_or_create_gif for each, and then append the return value from get_or_create_gif to the search term's associated gifs (remember, many-to-many relationship between search terms and gifs!).
    # If a new search term were created, it should finally be added and committed to the database.
    # And the SearchTerm instance should be returned.

def get_or_create_collection(name, gif_list, current_user):
    """Always returns a PersonalGifCollection instance"""
    pass
    # TODO 364: This function should get or create a personal gif collection. Uniqueness of the gif collection should be determined by the name of the collection and the id of the logged in user.
    # In other words, based on the input to this function, if there exists a collection with the input name, associated with the current user, then this function should return that PersonalGifCollection instance.
    # However, if no such collection exists, a new PersonalGifCollection instance should be created, and each Gif in the gif_list input should be appended to it (remember, there exists a many to many relationship between Gifs and PersonalGifCollections).
    # HINT: You can think of a PersonalGifCollection like a Playlist, and Gifs like Songs.

def get_gifs_from_giphy(search_string):
    """ Returns data from Giphy API with up to 5 gifs corresponding to the search input"""
    pass
    # TODO 364: This function should make a request to the Giphy API using the input search_string and your api_key (imported at the top of this file)
    # Then the function should process the request in order to return a list of 5 gif dictionaries.
    # HINT: You'll want to use 3 parameters in the API request -- api_key, q, and limit. You may need to do a bit of nested data investigation and look for API documentation.
    # HINT 2: test out this function outside your Flask application, in a regular simple Python program, with a bunch of print statements and sample invocations, to make sure it works!

########################
#### View functions ####
########################

## Error handling routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


## Login-related routes
@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))

@app.route('/register',methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now log in!')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/secret')
@login_required
def secret():
    return "Only authenticated users can do this! Try to log in or contact the site admin."

## Other routes
@app.route('/', methods=['GET', 'POST'])
def index():
    # TODO 364: Edit this view function so that the GifSearchForm is rendered.
    # If the form is submitted successfully:
    # invoke get_or_create_search_term on the form input and redirect to the function corresponding to the path /gifs_searched/<search_term> in order to see the results of the gif search.
    return render_template('index.html')

# Provided
@app.route('/gifs_searched/<search_term>')
def search_results(search_term):
    term = SearchTerm.query.filter_by(term=search_term)
    relevant_gifs = term.gifs.all()
    return render_template('searched_gifs.html',gifs=relevant_gifs)

# Provided
@app.route('/all_gifs')
def all_gifs():
    gifs = Gif.query.all()
    return render_template('all_gifs.html',all_gifs=gifs)

@app.route('/create_collection',methods=["GET","POST"])
@login_required
def create_collection():
    form = CollectionCreateForm()
    gifs = Gif.query.all()
    choices = [(g.id, g.title) for g in gifs]
    # TODO 364: Assign the choices list to the form's choices attribute
    # TODO 364: If the data from the form is successfully posted to this page, get the gifs that are selected from the form. You should find a list of ids that are each in string format.
    ## Cast each of those ids to an integer, and access the corresponding Gif instance by invoking your get_gif_by_id function. (HINT: You can do this in one line, with a list comprehension!)
    # TODO 364: Invoke the get_or_create_collection function on the current user, the appropriate submitted data from the form, and the list of gif objects you've just created in the previous TODO for this function.
    # If that is successful, redirect to the page showing all the current user's gif collections (at '/collections')

@app.route('/collections',methods=["GET","POST"])
@login_required



if __name__ == '__main__':
    db.create_all()
    manager.run()
