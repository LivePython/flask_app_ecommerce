from flask import redirect, session, current_app, render_template, url_for, request, flash
from shop import db, app, photos
from .forms import CustomerRegistrationForm
import secrets, os


@app.route('/customerregister')
def customer_register():
    return render_template('customers/register.html')