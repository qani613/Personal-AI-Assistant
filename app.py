from flask import Flask, render_template, redirect, url_for, session, flash, make_response
from flask_bootstrap import Bootstrap
from forms import LoginForm
import config

app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)

# Function to set no-cache headers
def no_cache(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.after_request
def apply_no_cache(response):
    return no_cache(response)

def authenticate_user(username, password):
    return username in config.USERS and config.USERS[username] == password

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if authenticate_user(username, password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/index')
def index():
    if 'username' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/')
def root():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
