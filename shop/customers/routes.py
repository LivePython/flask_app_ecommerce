from flask import redirect, session, current_app, render_template, url_for, request, flash
from shop import db, app, photos, search, bcrypt, login_manager
from .forms import CustomerRegistrationForm, CustomerLoginForm
import secrets, os
from .models import Register
from flask_login import login_required, current_user, login_user, logout_user


@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegistrationForm(request.form)
    try:
        if request.method == 'POST' or form.validate():
            hash_password = bcrypt.generate_password_hash(form.password.data)
            register = Register(
                name=form.name.data,
                username=form.username.data,
                email=form.email.data,
                password=hash_password,
                country=form.country.data,
                state=form.state.data,
                city=form.city.data,
                contact=form.contact.data,
                address=form.address.data,
                zipcode=form.zipcode.data,
            )
            db.session.add(register)
            db.session.commit()
            
            flash(f"Welcome {form.name.data}. Thank you for registering!", 'success')
            return redirect(url_for('login'))
            
        flash(f"Try Again", 'danger')
    except Exception as d:
        flash(f"Email address used", 'danger')
        return render_template('customers/register.html', form=form)
    return render_template('customers/register.html', form=form)
    
@app.route('/customer/login', methods=['GET', 'POST'])
def customerLogin():
    form = CustomerLoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash('Invalid email or password')  # Provide a more general message for security reasons
            return redirect(url_for('customerLogin'))
    return render_template('customers/login.html', form=form)


@app.route('/customer/logout')
def customer_logout():
    logout_user()
    flash('You are logged out!', 'warning')
    return redirect(url_for('customerLogin'))