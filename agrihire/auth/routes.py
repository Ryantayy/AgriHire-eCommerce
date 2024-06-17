from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from agrihire import my_hashing
from agrihire.auth.forms import LoginForm, RegisterForm, PasswordResetForm
from agrihire.utilities import get_user_by_email, user_exists_with_email, get_user_titles, hash_password, register_new_customer, reset_password,get_all_category,get_sub_category_by_category,get_all_stores
from datetime import datetime, timedelta, date

auth = Blueprint("auth", __name__, template_folder="templates")

@auth.context_processor
def inject_menu():
    categories = get_all_category()
    for category in categories:
        sub_categories = get_sub_category_by_category(category['category_id'])
        category['sub_categories'] = sub_categories
    stores = get_all_stores()
    return dict(inject_categories=categories, stores=stores)

def flash_form_errors(form):
    if form.errors:
        for error_messages in form.errors.values():
            for error in error_messages:
                flash(f"{error}", "danger")

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    user_titles = get_user_titles()
    form.title.choices = [(title, title) for title in user_titles]

    # When user clicks on submit button
    if form.validate_on_submit():
        title = form.title.data
        email = form.email.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        phone = form.phone.data
        password = form.password.data
        date_of_birth = form.date_of_birth.data
        address = form.address.data

        hashed_password = hash_password(password)

        # Register a new member
        register_new_customer(title, firstname, lastname, email, phone, hashed_password, date_of_birth, address)
        flash("You have registered successfully!", "success")
        return redirect(url_for('main.home'))

    categories = get_all_category()
    
    flash_form_errors(form)
    return render_template("register.html", form=form,categories= categories)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # No errors with the form valitor at this point
        email = form.email.data.lower()
        password = form.password.data
        remember_me = form.remember_me.data
        user = get_user_by_email(email)

        # Check if user exists (It should be already checked in forms but just in case).
        if not user:
            flash(f"No existing user with email: {email}", "danger")
            return redirect(url_for('auth.login'))

        # Check user password
        if check_password(user, password):
            login_user(user)
            flash("You have logged in successfully.", "success")

            if user['role_id'] == 1:
                return redirect(url_for('customer.dashboard'))
            elif user['role_id'] == 2:
                return redirect(url_for('staff.dashboard'))
            elif user['role_id'] == 3 or user['role_id']==5:
                return redirect(url_for('manager.dashboard'))
            elif user['role_id'] == 4:
                return redirect(url_for('admin.dashboard'))
            
        else:
            flash("Incorrect password.", "danger")

    categories = get_all_category()
    flash_form_errors(form)
    return render_template("login.html", form=form,categories = categories)

@auth.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    form = PasswordResetForm()

    if form.validate_on_submit():
        email = form.email.data.lower()
        user = get_user_by_email(email)
        password = form.password.data

        hashed_password = hash_password(password)
        if not user:
            flash(f"No existing user with email: {email}", "danger")
            return redirect(url_for('auth.forgot_password'))

        # Reset password
        reset_password(email, hashed_password)
        flash("Your password has been reset!", "success")
        return redirect(url_for('auth.login'))

    flash_form_errors(form)
    return render_template("forgot_password.html", form=form)

def login_user(user):
    session['loggedin'] = True
    session['email'] = user['email']
    session['role_id'] = user['role_id']
    session['user_id'] = user['user_id']

# logout
@auth.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("role_id", None)
    session.pop("email", None)
    session.pop("loggedin", None)
    
    flash("You have logged out successfully.", "success")
    return redirect(url_for("auth.login"))


def check_password(user, user_password):
    # Compare hashed password with the password stored in db
    db_password = user['password']
    if my_hashing.check_value(db_password, user_password, salt='myhashsalt'):
        return True
    else:
        return False
