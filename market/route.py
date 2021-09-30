from market import app
from market.database import Items, User
from market.forms import Register, Login, PurchaseItems, SellItems
from market import db
from flask import redirect, url_for, flash, render_template, request
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
@app.route("/home")
def homepage():
    return render_template('home.html')


@app.route("/market", methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItems()
    selling_form = SellItems()
    if request.method == 'POST':
        # Purchase
        purchased_items = request.form.get('purchased_items')
        p_item = Items.query.filter_by(name=purchased_items).first()
        if p_item:
            if current_user.budget_check(p_item):
                p_item.buy(current_user)
                flash(f"Congratulations! You have purchased {p_item.name}", category='success')
            else:
                flash(f"You have insufficient money", category='danger')
        #Sell
        sell_items = request.form.get('sold_items')
        s_item = Items.query.filter_by(name=sell_items).first()
        if s_item:
            if current_user.owner_check(s_item):
                s_item.sell(current_user)
                flash(f"Congratulations! {s_item.name} have been sold for {s_item.price}", category='success')
            else:
                flash(f"There are problems when trying to sell {s_item.name}!", category='danger')
        return redirect(url_for('market_page'))
    if request.method == 'GET':
        items = Items.query.filter_by(owner_id=None)
        owned_items = Items.query.filter_by(owner_id=current_user.id)
        return render_template('market.html', items=items,
                               purchase_form=purchase_form,
                               owned_items=owned_items,
                               sell_form=selling_form)


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form = Register()
    if form.validate_on_submit():
        user_creation = User(username=form.username.data,
                             email=form.email.data,
                             hash_password=form.password1.data)
        db.session.add(user_creation)
        db.session.commit()
        login_user(user_creation)
        flash(f"Registration is complete! You're login as {user_creation.username}", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for error_msg in form.errors.values():
            flash(f'There is error: {error_msg[0]}', category="danger")
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = Login()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.password_check(form.password.data):
            login_user(attempted_user)
            flash(f"You're login as {attempted_user}", category='success')
            return redirect(url_for('market_page'))
        else:
            flash(f"Username or password doesn't match", category='danger')
    return render_template('login.html', form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logout!", category='info')
    return redirect(url_for("homepage"))
