from flask import redirect, session, current_app, render_template, url_for, request, flash
from shop import db, app, photos, search, bcrypt
from .forms import CustomerRegistrationForm
import secrets, os
from .models import Register


@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegistrationForm(request.form)

    if request.method == 'POST' or form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=hash_password,
            confirm=form.confirm.data,
            country=form.country.data,
            state=form.state.data,
            city=form.city.data,
            contact=form.contact.data,
            address=form.address.data,
            zipcode=form.zipcode.data,
        )
        db.session.add(register)
        # db.session.commit()
        
        flash(f"Welcome {form.name.data}. Thank you for registering!", 'success')
        return redirect(url_for('login'))

    return render_template('customers/register.html', form=form)
