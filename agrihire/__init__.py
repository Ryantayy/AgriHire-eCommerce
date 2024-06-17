import os
from flask import Flask, session
from flask_hashing import Hashing
from datetime import timedelta
import pdfkit

app = Flask(__name__)
my_hashing = Hashing(app)


def create_app():

    app.secret_key = os.environ.get('SECRET_KEY') or "MySecretKey"

    # Configure the duration of the remember me cookie
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=14)

    # Config upload images 
    app.config['UPLOAD_FOLDER'] = 'agrihire/static/assets/images'  # Define where to store the uploaded files


    from agrihire.auth.routes import auth
    from agrihire.main.routes import main
    from agrihire.manager.routes import manager
    from agrihire.customer.routes import customer
    from agrihire.staff.routes import staff
    from agrihire.admin.routes import admin
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(staff, url_prefix="/staff")
    app.register_blueprint(customer, url_prefix="/customer")
    app.register_blueprint(manager, url_prefix="/manager")
    app.register_blueprint(admin, url_prefix="/admin")
    
    return app
