from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from datetime import datetime
from agrihire.admin.forms import mainCategory,subCategory,EditSubCategoryForm,StoreForm,editAdminProfileForm,changePasswordForm,addNationalManagerForm,editNationalManagerForm
from agrihire.utilities import add_category,get_all_category,add_Image,count_num_of_sub_category,insert_sub_category,get_all_sub_category_details, get_sub_category_details_by_id, update_sub_category,get_images_by_sub_category_id,get_all_stores_with_managers, add_store_function, get_all_local_managers, add_Image, get_store_by_id, update_store,update_admin_profile,get_user_titles,get_admin_by_user_id,get_user_by_email,hash_password,reset_password,get_national_manager,add_national_manager,delete_national_manager_sql,update_national_manager_sql,get_national_manager_details_by_user_id

import os
from agrihire import app
from werkzeug.utils import secure_filename
from agrihire.auth.routes import check_password

admin = Blueprint("admin", __name__, template_folder="templates")


# region functions
def check_auth():
    if not 'loggedin' in session:
        flash("Please login first.", "danger")
        return redirect(url_for('auth.login'))

    if session['role_id'] != 4:
        flash("Invalid action! Back to home page.", "danger")
        return redirect(url_for('main.home'))
    return None

def flash_form_errors(form):
    if form.errors:
        for error_messages in form.errors.values():
            for error in error_messages:
                flash(f"{error}", "danger")
                
def format_timedelta(delta):
    # A datetime object for midnight of a given day
    midnight = datetime.combine(datetime.today(), datetime.min.time())
    # Add the timedelta to midnight to get a datetime object
    datetime_with_delta = midnight + delta
    # Extract the time component
    time = datetime_with_delta.time()
    return time

# endregion

# region routes

@admin.route("/dashboard", methods=["GET"])
def dashboard():
    # Check authentication and authorisation
    auth_response = check_auth()
    if auth_response:
        return auth_response
    return render_template("admin_main_dashboard.html", page_name='dashboard')

@admin.route("/admin_account_settings", methods=["GET", "POST"])
def admin_account_settings():
    form = editAdminProfileForm()
    password_form = changePasswordForm() 
    user = get_admin_by_user_id(session['user_id'])

    user_titles = get_user_titles()
    form.title.choices = [(title, title) for title in user_titles]

    if form.validate_on_submit():
        title = form.title.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        phone = form.phone.data
        address = form.address.data

        # Update the user profile
        update_admin_profile(title, firstname, lastname, email, phone, address)
        session['email'] = email
        flash("Profile updated successfully!", "success")
        return redirect(url_for('admin.admin_account_settings'))
    else:
        form.title.data = user['title']
        form.firstname.data = user['first_name']
        form.lastname.data = user['last_name']
        form.original_email.data = user['email']
        form.email.data = user['email']
        form.phone.data = user['phone']
        form.address.data = user['address']

    flash_form_errors(form)
    return render_template("admin_profile.html", form=form, password_form=password_form)

@admin.route("/change_password", methods=["GET", "POST"])
def change_password():
    # Check authentication and authorisation
    auth_response = check_auth()
    if auth_response:
        return auth_response

    #Retrieve user details
    form = editAdminProfileForm()
    user = get_admin_by_user_id(session['user_id'])
    user_titles = get_user_titles()
    form.title.choices = [(title, title) for title in user_titles]

    form.title.data = user['title']
    form.firstname.data = user['first_name']
    form.lastname.data = user['last_name']
    form.original_email.data = user['email']
    form.email.data = user['email']
    form.phone.data = user['phone']
    form.address.data = user['address']

    password_form = changePasswordForm()
    
    if password_form.validate_on_submit():
        email = session['email']
        current_password = password_form.current_password.data
        new_password = password_form.new_password.data

        # Check if the current password is correct
        email = session['email']
        user = get_user_by_email(email)
        if check_password(user, current_password):
            hashed_password = hash_password(new_password)
            reset_password(email, hashed_password)
            flash("Password changed successfully!", "success")
        else:
            flash("Incorrect password.", "danger")

        return redirect(url_for('admin.dashboard'))

    flash_form_errors(password_form)
    return render_template("admin_profile.html", form=form, password_form=password_form)
   
@admin.route("/add_main_category", methods=["GET", "POST"])
def add_main_category():
    
    auth_response = check_auth()
    if auth_response:
        return auth_response
    
    form = mainCategory()
    
    if form.is_submitted() and form.validate():
        category_name = form.category_name.data
        
        add_category(category_name)
        
        flash("Category added successfully!", "success")
        return redirect(url_for('admin.dashboard'))
    
    flash_form_errors(form) 
    return render_template("admin_add_main_category.html",form = form)
   
@admin.route("/add_sub_category", methods=["GET", "POST"])
def add_sub_category():
    
    auth_response = check_auth()
    if auth_response:
        return auth_response
    
    form = subCategory()
    
    category_list = get_all_category()
    form.category.choices = [(category['category_id'], category['category_name']) for category in category_list]
    
    if form.is_submitted() and form.validate():
    
        name = form.name.data
        hire_cost = form.hire_cost.data
        description = form.description.data
        weight = form.weight.data
        dimension = form.dimension.data
        shipping_price = form.shipping_price.data
        category_id = form.category.data
        
        images = request.files.getlist('product_images')
        
        # calculate the next sub category id
        sub_category_id = int(count_num_of_sub_category()['count']) +1
        
        # if there are some images uploaded
        if images and images[0]:
           for image in images:
               filename = f"sub-{sub_category_id}-{secure_filename(image.filename)}"
               file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'products',filename)

               # Create directory if it does not exist
               os.makedirs(os.path.dirname(file_path), exist_ok=True)

               image.save(file_path)
            
               add_Image(sub_category_id, 1, 'equipment', filename)
        
        flash("Sub category added successfully!", "success")    
        insert_sub_category(category_id, name, hire_cost,sub_category_id, description, weight, dimension, shipping_price)
        
        return redirect(url_for('admin.dashboard'))
    
    flash_form_errors(form) 
    return render_template("admin_add_sub_category.html",form = form)
   
@admin.route("/equipments", methods=["GET", "POST"])
def equipments():
       return render_template("admin_equipments.html")
   
@admin.route("/sub_categories", methods=["GET", "POST"])
def sub_categories():
    sub_categories = get_all_sub_category_details()
    return render_template("admin_sub_categories.html", sub_categories=sub_categories)
    
@admin.route("/edit_subcategory/<int:sub_category_id>", methods=["GET", "POST"])
def edit_subcategory(sub_category_id):
    form = EditSubCategoryForm()
    sub_categories = get_all_sub_category_details()
    sub_category_details = get_sub_category_details_by_id(sub_category_id)
    
    if form.validate_on_submit():
        hire_cost = form.hire_cost.data
        shipping_price = form.shipping_price.data
        min_hire_period = form.min_hire_period.data
        max_hire_period = form.max_hire_period.data
        
        # Update the sub category
        update_sub_category(hire_cost, shipping_price, min_hire_period, max_hire_period, sub_category_id)

        flash("Sub Category updated successfully!", "success")
        sub_categories = get_all_sub_category_details()
        return render_template("admin_sub_categories.html", sub_categories=sub_categories)
    else:
        form.category.data = sub_category_details['category_name']
        form.subcategory.data = sub_category_details['sub_category_name']
        form.weight.data = sub_category_details['weight']
        form.dimension.data = sub_category_details['dimension']
        form.description.data = sub_category_details['description']
        form.hire_cost.data = sub_category_details['hire_cost']
        form.shipping_price.data = sub_category_details['shipping_price']
        form.min_hire_period.data = sub_category_details['min_hire_period']
        form.max_hire_period.data = sub_category_details['max_hire_period']
        sub_category_id = sub_category_details['sub_category_id']
        
        image_url = get_images_by_sub_category_id(sub_category_id)

    return render_template("edit_subcategory.html", sub_categories=sub_categories, form=form, sub_category_id=sub_category_id, image = image_url)


@admin.route("/search", methods=["GET", "POST"])
def search():
    search_query = request.args.get('search_query')
    sub_categories = get_all_sub_category_details()
    if search_query:
       results = [sc for sc in sub_categories if search_query.lower() in sc['sub_category_name'].lower() or search_query.lower() in sc['category_name'].lower()]
    else:
       results = []
    return render_template("admin_sub_categories.html", sub_categories=results)

@admin.route("/managers", methods=["GET", "POST"])
def managers():   
    auth_response = check_auth()
    if auth_response:
        return auth_response
    
    national_managers = get_national_manager()
     
    return render_template("admin_managers.html", national_managers = national_managers)



@admin.route("/stores/add", methods=['GET', 'POST'])
def add_store():
    form = StoreForm()

    if form.validate_on_submit():
        store_name = form.store_name.data
        address = form.address.data

        image_id = None
        if form.image.data:
            image_file = form.image.data
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'stores-logo', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            image_file.save(file_path)

            relative_image_url = f'{filename}'
            image_id = add_Image(sub_category_id=0, entity_id=6, entity_type='store', image_url=relative_image_url)

        try:
            add_store_function(store_name, address, image_id)
            flash("New store added successfully!", "success")
            return redirect(url_for('admin.stores'))
        except Exception as e:
            flash(f"Failed to add store: {str(e)}", "danger")

    return render_template("admin_add_store.html", form=form)


@admin.route('/stores/edit/<int:store_id>', methods=['GET', 'POST'])
def edit_store(store_id):
    store = get_store_by_id(store_id)
    if not store:
        flash('Store not found!', 'danger')
        return redirect(url_for('admin.stores'))
    
    form = StoreForm(obj=store)
    
    if form.validate_on_submit():
        store_name = form.store_name.data
        address = form.address.data
        image_file = form.image.data
        
        image_id = store.get('image_id')

        if image_file:
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'stores-logo', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            image_file.save(filepath)

            image_id = add_Image(sub_category_id=0, entity_id=6, entity_type='store', image_url=filename)

        try:
            update_store(store_id, store_name, address, image_id)
            flash('Store updated successfully!', 'success')
            return redirect(url_for('admin.stores'))
        except Exception as e:
            flash(f'Failed to update store: {e}', 'danger')
    
    return render_template('admin_edit_store.html', form=form, store=store)

@admin.route("/stores", methods=["GET"])
def stores(): 
    if check_auth():
        return check_auth()
    stores = get_all_stores_with_managers()  # Fetch data using a utility function
    return render_template("admin_stores.html", stores=stores)

@admin.route("/edit_national_manager/<int:user_id>", methods=["GET","POST"])
def edit_national_manager(user_id):
    auth_response = check_auth()
    if auth_response:
        return auth_response
    
    user = get_national_manager_details_by_user_id(user_id)

    form = editNationalManagerForm()
    user_titles = get_user_titles()
    form.title.choices = [(title, title) for title in user_titles]
    
    if form.validate_on_submit():
        title_id = form.title.data
        email = form.email.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        phone = form.phone.data
        address = form.address.data
        password = form.password.data
       
        update_national_manager_sql(title_id, firstname, lastname, email, phone, address, password,user_id)
        flash("National Manager updated successfully.", "success")

  
        national_managers = get_national_manager()
        return render_template("admin_managers.html", national_managers=national_managers)
    else:
        form.title.data = user['title']
        form.firstname.data = user['first_name']
        form.lastname.data = user['last_name']
        form.email.data = user['email']
        form.phone.data = user['phone']
        form.address.data = user['address']
        form.original_email.data = user['email']
    
    
    flash_form_errors(form)
    return render_template("admin_edit_national_manager.html",form = form, user_id=user_id)

@admin.route("/delete_national_manager/<int:user_id>", methods=["GET","POST"])
def delete_national_manager(user_id):
    try:
       delete_national_manager_sql(user_id)
    except:
        flash_form_errors("Something wrong during delete this national manager.")
 
    flash("Successfully delete this national manager")
 
    national_managers = get_national_manager()
    return render_template("admin_managers.html",national_managers = national_managers)

@admin.route("/add_new_national_manager", methods=["GET","POST"])
def add_new_national_manager():
    auth_response = check_auth()
    if auth_response:
        return auth_response

    form = addNationalManagerForm()
    user_titles = get_user_titles()
    form.title.choices = [(title, title) for title in user_titles]
    
    if form.validate_on_submit():
        title_id = form.title.data
        email = form.email.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        phone = form.phone.data
        address = form.address.data
        password = form.password.data
       
        add_national_manager(title_id, email, firstname, lastname, phone, address, password)
        flash("National Manager added successfully.", "success")

        national_managers = get_national_manager()
        return render_template("admin_managers.html", national_managers=national_managers)
    flash_form_errors(form)
    return render_template("admin_add_national_manager.html", form=form)

# endregion