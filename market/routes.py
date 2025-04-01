from market import app
from flask import render_template, redirect, url_for, request, flash, get_flashed_messages
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        #Purchase item logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$",
                      category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!",
                      category='danger')
        #Sell item logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name = sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You Sold {s_item_object.name} for {s_item_object.price}$",
                      category='success')
            else:
                flash(f"Somthing Went wrong with selling {s_item_object.name}!",
                      category='danger')
        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    print("\n=== DEBUG SUBMISSION STATE ===")
    # Debug print to show form submission state
    print(f"Request method: {request.method}")
    print(f"Form submitted: {form.is_submitted()}")
    print(f"Form validated: {form.validate()}\n")

    if form.validate_on_submit():
        print("\n=== FORM VALIDATION ===")
        print("Form validation passed!")
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category="success")
        return redirect(url_for('market_page'))

    # Only show errors after actual submission
    if request.method == 'POST' and form.errors:
        print("\n=== FORM ERRORS ===")
        print(f"Total errors: {len(form.errors)}")
        for field_name, errors in form.errors.items():
            for error in errors:
                print(f"Field '{field_name}': {error}")
                flash(f"Field '{field_name}': {error}", category='danger')
    else:
        print("\n=== FORM ERRORS ===")
        print("No form errors detected\n")

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form= LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not correct! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))