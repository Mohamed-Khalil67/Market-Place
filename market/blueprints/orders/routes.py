import stripe
from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from market import db
from market.models import Item, CartItem, Order, OrderItem
from market.blueprints.orders import orders_bp

@orders_bp.route('/checkout')
@login_required
def checkout():
    cart_items = current_user.cart_items
    
    if not cart_items:
        flash('Your cart is empty', category='danger')
        return redirect(url_for('cart.cart_page'))
    
    return render_template('orders/checkout.html', cart_items=cart_items)

@orders_bp.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    cart_items = current_user.cart_items
    
    if not cart_items:
        flash('Your cart is empty', category='danger')
        return redirect(url_for('cart.cart_page'))
    
    # Create order in pending state
    order = Order(
        user_id=current_user.id,
        total_amount=current_user.cart_total,
        status='pending'
    )
    
    # Add order items
    for cart_item in cart_items:
        order_item = OrderItem(
            item_id=cart_item.item_id,
            quantity=cart_item.quantity,
            price=cart_item.item.price
        )
        order.items.append(order_item)
    
    db.session.add(order)
    db.session.commit()
    
    # Create line items for Stripe
    line_items = []
    for cart_item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': cart_item.item.name,
                    'description': cart_item.item.description[:100],
                },
                'unit_amount': cart_item.item.price * 100,  # Stripe uses cents
            },
            'quantity': cart_item.quantity,
        })
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=url_for('orders.order_success', order_id=order.id, _external=True),
            cancel_url=url_for('orders.order_cancel', order_id=order.id, _external=True),
            metadata={
                'order_id': order.id
            }
        )
        
        # Update order with session ID
        order.payment_id = checkout_session.id
        db.session.commit()
        
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return jsonify(error=str(e)), 403

@orders_bp.route('/success/<int:order_id>')
@login_required
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Verify the order belongs to the current user
    if order.user_id != current_user.id:
        flash('Unauthorized access', category='danger')
        return redirect(url_for('main.home_page'))
    
    # Clear the cart
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    
    return render_template('orders/success.html', order=order)

@orders_bp.route('/cancel/<int:order_id>')
@login_required
def order_cancel(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Verify the order belongs to the current user
    if order.user_id != current_user.id:
        flash('Unauthorized access', category='danger')
        return redirect(url_for('main.home_page'))
    
    # Update order status
    order.status = 'cancelled'
    db.session.commit()
    
    return render_template('orders/cancel.html', order=order)

@orders_bp.route('/history')
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders/history.html', orders=orders)

@orders_bp.route('/webhook', methods=['POST'])
def webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, current_app.config['STRIPE_WEBHOOK_SECRET']
        )
    except ValueError as e:
        # Invalid payload
        return jsonify(success=False), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return jsonify(success=False), 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Retrieve the order
        order_id = session.get('metadata', {}).get('order_id')
        if order_id:
            order = Order.query.get(order_id)
            if order:
                # Update order status
                order.status = 'paid'
                
                # Process the order (e.g., transfer ownership of items)
                for order_item in order.items:
                    item = order_item.item
                    if item.owner != order.user_id:
                        # Transfer ownership
                        item.owner = order.user_id
                
                db.session.commit()
    
    return jsonify(success=True)
