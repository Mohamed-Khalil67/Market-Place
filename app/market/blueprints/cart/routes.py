from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from market import db
from market.models import Item, CartItem
from market.blueprints.cart import cart_bp

@cart_bp.route('/')
@login_required
def cart_page():
    cart_items = current_user.cart_items
    return render_template('cart/cart.html', cart_items=cart_items)

@cart_bp.route('/add/<int:item_id>', methods=['POST'])
@login_required
def add_to_cart(item_id):
    item = Item.query.get_or_404(item_id)
    quantity = int(request.form.get('quantity', 1))
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(user_id=current_user.id, item_id=item_id).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=current_user.id, item_id=item_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f'Added {item.name} to your cart!', category='success')
    return redirect(url_for('products.product_list'))

@cart_bp.route('/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, item_id=item_id).first_or_404()
    quantity = int(request.form.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
    else:
        db.session.delete(cart_item)
    
    db.session.commit()
    return redirect(url_for('cart.cart_page'))

@cart_bp.route('/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, item_id=item_id).first_or_404()
    db.session.delete(cart_item)
    db.session.commit()
    return redirect(url_for('cart.cart_page'))
