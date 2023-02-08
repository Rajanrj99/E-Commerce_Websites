from flask import render_template, Blueprint, redirect, url_for, request, flash
from website import db
from .models.item import Item
from .models.user import User
from flask_login import login_user, login_required, logout_user, current_user
from .forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm, AddItemForm


views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    return render_template('home.html')


@views.route('/market', methods=['GET', 'POST'])
@login_required
def market():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()

    if request.method == "POST":
        # puchase item logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(
                    f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$", category='success')
            else:
                flash(
                    f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')

    # Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(
                    f"Congratulations! You sold {s_item_object.name} back to market!", category='success')
            else:
                flash(
                    f"Something went wrong with selling {s_item_object.name}", category='danger')

        return redirect(url_for('views.market'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)


@views.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    print("hel")

    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(
            f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('views.market'))

    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(
                f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@views.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():

        attempted_user = User.query.filter_by(
            username=form.username.data).first()
        password = form.password.data

        if attempted_user:
            if attempted_user.password == password:

                login_user(attempted_user)
                flash(
                    f'Success! You are logged in as: {attempted_user.username}', category='success')
                return redirect(url_for('views.market'))
            else:
                flash('password are not match! Please try again', category='danger')
        else:
            flash('username not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@views.route('/add_items', methods=['GET', 'POST'])
def add_items():
    form = AddItemForm()
    if form.validate_on_submit():
        br = []
        for item in Item.query.with_entities(Item.barcode).all():
            br.append(item[0])

        if form.barcode.data not in br:

            user_to_create = Item(name=form.name.data,
                                  barcode=form.barcode.data,
                                  price=form.price.data)
            db.session.add(user_to_create)
            db.session.commit()

            flash(f"Item  successfully!", category='success')
            return redirect(url_for('views.market'))
        else:
            flash(
                f"Something went wrong with adding item: name or barcode already exist", category='danger')

    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(
                f'There was an error with adding a item: {err_msg}', category='danger')

    return render_template('add_items.html', form=form)


@views.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("views.home"))
