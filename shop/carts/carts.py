from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app
from shop.products.models import Addproduct
from shop.products.routes import brands, categories


def mergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2

    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items())+list(dict2.items()))

    return False
    
    
@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        colors = request.form.get('colors')
        product = Addproduct.query.filter_by(id=product_id).first()
        
        
        if  request.method == "POST":
            DictItems = {
                product_id:{
                    'name': product.name,
                    'price': product.price,
                    'discount': product.discount,
                    'colors': product.colors,
                    'quantity': quantity,
                    'image': product.image_1
                }
            }
            if "Shoppingcart" in session:

                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                    
                else:
                    session['Shoppingcart'] = mergeDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)

            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
            
    except Exception as a:
        print(a)
    finally:
        return redirect(request.referrer)


@app.route('/carts')
def getcarts():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) == 0:
        return redirect(url_for('home'))
    
    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        discount = float(product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) *int(product['quantity'])
        subtotal -= discount
        tax = ("%.2f" % (.06 * float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))    
    return render_template("products/carts.html", tax=tax, grandtotal=grandtotal, brands=brands(), categories=categories())



@app.route('/updatecart/<int:code>', methods=["POST"])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) == 0:
        return redirect(url_for('home'))
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash("Item is updated", 'success')
                    return redirect(url_for('getcarts'))
        except Exception as e:
            print(e)
            return redirect(url_for('getcarts'))


@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    try:
        if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
            return redirect(url_for('home'))
        
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == id:
                    session['Shoppingcart'].pop(key, None)
                    return redirect(url_for('getcart'))

        except Exception as a:
            print(a)
            return redirect(url_for('getcarts'))
    except:
        return redirect(url_for('home'))


@app.route('/clearcart')
def clearcart():
    try:
        if 'Shoppingcart' in session or len(session['Shoppingcart']) > 0:
            session.pop('Shoppingcart', None)
            return redirect(url_for('home'))
        
        return redirect(url_for("home"))
    except Exception as e:
        print(e)
        return redirect(url_for('home'))