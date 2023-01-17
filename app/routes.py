from app import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm,LoginForm, Newinfo
from app.models import User, Address

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Form Submitted and Validated!')
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(first_name, last_name, email, username, password)
        check_user = User.query.filter( (User.username == username) | (User.email == email) ).all()
        if check_user is not None:
            flash(f'{username} is already in your contacts', 'thank you')
            return redirect(url_for('signup'))

        new_user = User(first_name = first_name, last_name = last_name, email=email, username=username, password=password)
        flash(f'{new_user.username} has been added to your contacts')
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(username, password)
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f"{user.username} is now logged in", "warning")
            return redirect(url_for('address'))
        else:
            flash("Incorrect username and/or password", "danger")
            return redirect(url_for('index'))
        
    return render_template('index.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", "warning")
    return redirect(url_for('index'))

@app.route('/allcontacts')
def contacts():
    contacts= Address.query.all()
    return render_template('contact.html', contacts = contacts)

@app.route('/create-contact', methods=['GET', 'POST'])
@login_required
def create_contact():
    form = Newinfo()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name= form.last_name.data
        phone_number = form.phone_number.data
        address = form.address.data
        new_contact = Address(first_name=first_name, last_name=last_name, phone_number = phone_number, address = address, user_id=current_user.id)
        flash(f"{new_contact.first_name} {new_contact.last_name}has been created", "success")
        return redirect(url_for('index'))
        
    return render_template('create.html', form=form)

@app.route('/create-contact/<int:address_id>')
def get_post(address_id):
    contact = Address.query.get(address_id)
    if not contact:
        flash(f"A post with id {address_id} does not exist", "danger")
        return redirect(url_for('index'))
    return render_template('post.html', contact=contact)

