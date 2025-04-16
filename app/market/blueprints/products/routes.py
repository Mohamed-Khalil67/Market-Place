from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from market import db, cache
from market.models import Item, Category
from market.blueprints.products import products_bp
from market.blueprints.products.forms import ProductForm, CategoryForm
import os
from werkzeug.utils import secure_filename
import uuid

def save_image(image_file):
    random_hex = uuid.uuid4().hex
    _, file_extension = os.path.splitext(image_file.filename)
    image_filename = random_hex + file_extension
    image_path = os.path.join(current_app.root_path, 'static/product_images', image_filename)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    
    image_file.save(image_path)
    return f'product_images/{image_filename}'

@products_bp.route('/')
@login_required
@cache.cached(timeout=60, key_prefix='product_list')
def product_list():
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Number of items per page
    
    items = Item.query.filter_by(owner=None).paginate(page=page, per_page=per_page)
    owned_items = Item.query.filter_by(owner=current_user.id).paginate(page=page, per_page=per_page)
    
    return render_template('products/list.html', items=items, owned_items=owned_items)

@products_bp.route('/search')
@login_required
def search():
    query = request.args.get('query', '')
    category_id = request.args.get('category', '')
    
    items_query = Item.query
    
    if query:
        items_query = items_query.filter(
            (Item.name.contains(query)) | 
            (Item.description.contains(query))
        )
    
    if category_id and category_id.isdigit():
        items_query = items_query.filter_by(category_id=int(category_id))
    
    items = items_query.all()
    categories = Category.query.all()
    
    return render_template(
        'products/search_results.html', 
        items=items, 
        categories=categories, 
        query=query, 
        selected_category=category_id
    )

@products_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        image_url = None
        if form.image.data:
            image_url = save_image(form.image.data)
            
        new_item = Item(
            name=form.name.data,
            price=form.price.data,
            barcode=form.barcode.data,
            description=form.description.data,
            category_id=form.category.data,
            stock=form.stock.data,
            image_url=image_url,
            owner=current_user.id
        )
        
        db.session.add(new_item)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('products.product_list'))
        
    return render_template('products/add_product.html', form=form, title='Add Product')

@products_bp.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    form = CategoryForm()
    
    if form.validate_on_submit():
        new_category = Category(
            name=form.name.data,
            description=form.description.data
        )
        
        db.session.add(new_category)
        db.session.commit()
        flash('Category added successfully!', 'success')
        return redirect(url_for('products.categories'))
        
    categories = Category.query.all()
    return render_template('products/categories.html', form=form, categories=categories, title='Categories')

@products_bp.route('/detail/<int:item_id>')
@login_required
def product_detail(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('products/detail.html', item=item, title=item.name)
