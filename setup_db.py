from flask import Flask
from market import create_app, db
from market.models import User, Item, Category, CartItem, Order, OrderItem
import os

# Create a Flask application with the development configuration
app = create_app('development')

# Define a function to create a sample database with test data
def create_sample_data():
    # Create categories
    electronics = Category(name="Electronics", description="Electronic devices and gadgets")
    clothing = Category(name="Clothing", description="Apparel and fashion items")
    books = Category(name="Books", description="Books and publications")
    
    # Add categories to session
    db.session.add_all([electronics, clothing, books])
    db.session.commit()
    
    # Create sample items
    items = [
        Item(
            name="Smartphone", 
            price=499, 
            barcode="123456789012", 
            description="Latest smartphone with high-resolution camera and fast processor",
            category_id=electronics.id,
            stock=10
        ),
        Item(
            name="Laptop", 
            price=899, 
            barcode="234567890123", 
            description="Powerful laptop with SSD storage and high-performance CPU",
            category_id=electronics.id,
            stock=5
        ),
        Item(
            name="T-shirt", 
            price=25, 
            barcode="345678901234", 
            description="Comfortable cotton t-shirt available in multiple colors",
            category_id=clothing.id,
            stock=20
        ),
        Item(
            name="Jeans", 
            price=45, 
            barcode="456789012345", 
            description="Classic denim jeans with modern fit",
            category_id=clothing.id,
            stock=15
        ),
        Item(
            name="Python Programming", 
            price=35, 
            barcode="567890123456", 
            description="Comprehensive guide to Python programming language",
            category_id=books.id,
            stock=8
        ),
        Item(
            name="Web Development", 
            price=40, 
            barcode="678901234567", 
            description="Learn modern web development techniques and frameworks",
            category_id=books.id,
            stock=7
        )
    ]
    
    # Add items to session
    db.session.add_all(items)
    
    # Create a test user
    test_user = User(
        username="testuser",
        email_address="test@example.com",
        password="Password123!",
        budget=1000
    )
    
    db.session.add(test_user)
    db.session.commit()
    
    print("Sample data created successfully!")

if __name__ == '__main__':
    with app.app_context():
        # Create all database tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Ask if user wants to create sample data
        create_sample = input("Do you want to create sample data? (y/n): ")
        if create_sample.lower() == 'y':
            create_sample_data()
