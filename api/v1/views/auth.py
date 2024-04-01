""" Objects that handle all default RestFul API actions for Users:
    - Signup
    - Login
    - Logout
    - User generate Session
"""
from validate_email import validate_email
from flask import flash, render_template, url_for, redirect, session, request, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from models.user import User
from models.article import Article
from database import db

# BLUEPRINT
auth = Blueprint('auth', __name__, url_prefix='/auth')



def is_authenticated():
    """Check if user is authenticated"""
    return 'user_id' in session


@auth.before_request
def require_login():
    protected_routes = ['/generate']
    if request.path in protected_routes and not is_authenticated():
        flash('Kindly login to access generate')
        return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def signup():
    """Signup logic"""
    if request.method == 'POST':
        email = request.form.get('email')

        if not validate_email(email, check_mx=False):
            return jsonify({'message': 'Invalid Credentials', 'status': 'error'})

        password_hash = generate_password_hash(request.form.get('password'))
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')

        existing_user = db.session.query(User).filter_by(email=email).first()
        try:
            if existing_user:
                return jsonify({'message': 'An account with this email already exists. Try logging in?', 'status': 'error'})
            elif not email or not password_hash or not firstname:
                return jsonify({'message': 'Missing credentials.', 'status': 'error'})
            else:
                new_user = User(email=email,
                                password_hash=password_hash,
                                firstname=firstname,
                                lastname=lastname)

                db.session.add(new_user)
                db.session.commit()
                return jsonify({'message': 'Account created successfully. Redirecting to login.', 'status': 'success'})
        except Exception as e:
            print(f"Exception: {e}")
            db.session.rollback()
            return jsonify({'message': 'There was a problem creating your account. Try again.', 'status': 'error'})


@auth.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """Login Logic"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = db.session.query(User).filter_by(email=email).first()

        if not user:
            return jsonify({'message': 'Oops, Looks like you do not have an account. Kindly create one.', 'status': 'error'})
        elif not check_password_hash(user.password_hash, password):
            return jsonify({'message': 'Incorrect password. Please try again!', 'status': 'error'})
        else:
            session['user_id'] = user.id  # Storing user id in session
            return jsonify({'message': f'Welcome {user.firstname}', 'status': 'success'})
    return render_template('login.html')


@auth.route('/get_username', methods=['GET'], strict_slashes=False)
def username():
    """Query user's firstname"""
    if 'user_id' in session:
        user_id = session['user_id']
        user = db.session.query(User).filter(User.id == user_id).first()
        if user:
            return jsonify({'username': user.firstname})
        else:
            return jsonify({'error': 'User not found'})
    return jsonify({'error': 'User not authenticated'})


@auth.route('/logout', methods=['GET', 'POST'], strict_slashes=False)
def logout():
    """Logout logic"""
    session.pop('user_id', None)
    message = 'You have been logged out successfully.'
    flash(message)
    return redirect(url_for('auth.login'))
