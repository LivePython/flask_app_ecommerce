from flask import redirect, session, current_app, render_template, url_for, request, flash
from shop import db, app, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets, os


@app.route('/')
def home():
    # Pagination
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).paginate(page=page, per_page=4)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html', brands=brands, products=products, categories=categories)

@app.route('/brand/<int:id>')
def get_brand(id):
    get_brand_product = Addproduct.query.filter_by(brand_id=id)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html', brand=get_brand_product, brands=brands, categories=categories)

@app.route('/categories/<int:id>')
def get_category(id):
    get_cat_product = Addproduct.query.filter_by(category_id=id)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html', cat=get_cat_product, brands=brands, categories=categories)
@app.route('/addbrand', methods=["GET", "POST"])
def addbrand():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f"The brand {getbrand} was added to your database", "success")
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands='brands')

@app.route('/updatebrand/<int:id>', methods=["GET", "POST"])
def updatebrand(id):
    if 'email' not in session:
        flash("Pleasen login first", 'danger')
        return render_template(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == 'POST':
        updatebrand.name = brand
        flash("Your brand has been updated", 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', updatebrand=updatebrand, title="Update Brand")

@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
        flash(f"The brand {brand.name} was deleted from your datbase", 'success')
        return redirect(url_for('brands'))
    flash(f"The brand {brand.name} can't deleted from your datbase", 'success')
    return redirect(url_for('brands'))

@app.route('/addcategory', methods=["GET", "POST"])
def addcategory():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getcategory = request.form.get('category')
        category = Category(name=getcategory)
        db.session.add(category)
        flash(f"The category {getcategory} was added to your database", "success")
        db.session.commit()
        return redirect(url_for('addcategory'))
    return render_template('products/addbrand.html', categories='category')


@app.route('/updatecat/<int:id>', methods=["GET", "POST"])
def updatecat(id):
    if 'email' not in session:
        flash("Pleasen login first", 'danger')
        return render_template(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == 'POST':
        updatecat.name = category
        flash("Your category has been updated", 'success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html', updatecat=updatecat, title="Update Category")


@app.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        flash(f"The brand {category.name} was deleted from your datbase", 'success')
        return redirect(url_for('category'))
    flash(f"The brand {category.name} can't deleted from your datbase", 'success')
    return redirect(url_for('category'))

    
@app.route("/addproduct", methods=["GET", "POST"])
def addproduct():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.description.data
        brand = request.form.get("brand")
        category = request.form.get('category')
        try:
            image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
            image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
            image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")
        except:
            flash(f"You must provide three images of product", 'warning')
            return redirect(url_for('addproduct'))
        addproduct = Addproduct(name=name, 
                                 price=price,
                                 discount=discount,
                                 stock=stock,
                                 colors=colors,
                                 description=desc,
                                 brand_id=brand,
                                 category_id=category,
                                 image_1=image_1,
                                 image_2=image_2,
                                 image_3=image_3)
        db.session.add(addproduct)
        flash(f"The product {name} is added successfully to your database", 'success')
        db.session.commit()
        return redirect(url_for("admin"))
    return render_template('products/addproduct.html', form=form, brands=brands, categories=categories, title="Add Product page")

@app.route("/updateproduct/<int:id>", methods=["GET", "POST"])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    form = Addproducts(request.form)

    brand = request.form.get('brand')
    category =request.form.get('category')

    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.colors = form.colors.data
        product.description = form.description.data
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')
            except:
               product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')
            except:
               product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')
            except:
               product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')
            
        db.session.commit()
        flash(f'Your product has been updates', 'success')
        return redirect(url_for('admin'))
    
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.description.data = product.description
    return render_template('products/updateproduct.html', form=form, brands=brands, categories=categories, 
                           product=product)

@app.route("/deleteproduct/<int:id>", methods=["GET", "POST"])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method == 'POST':
        try:
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_2))
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_3))
            product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')
        except Exception as a:
            print(a)
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('admin'))
