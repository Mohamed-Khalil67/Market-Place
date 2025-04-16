# Flask Marketplace

A full-featured online marketplace built with Flask where users can register, login, buy, and sell items.

![Marketplace Screenshot](market/static/images/market.png)

## Features

- **User Authentication**
  - Secure registration and login system
  - Password hashing with Werkzeug
  - Session management

- **Marketplace Functionality**
  - Browse available items
  - Post items for sale
  - Purchase items from other users
  - User dashboard to manage listings

- **Database**
  - SQLAlchemy ORM
  - SQLite (or PostgreSQL/MySQL ready)
  - Models for Users, Items, Transactions

- **Additional Features**
  - Responsive design
  - Form validation
  - Flash messaging
  - Admin dashboard (optional)

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, Bootstrap
- **Database**: SQLAlchemy, SQLite
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Mohamed-Khalil67/Market-Place.git
   cd flask-marketplace


### Notes
- export FLASK_APP=market.py
  - define flask variable to run
- export FLASK_DEBUG=1 
  - constant debug of your web application
- SQLALCHEMY_DATABASE_URI
  - URI = Uniform Resource Identifier
- href="{{ url_for('register_page') }}"
  - Calls the function name in the route if route is changed , url inside stays the same

#### 1- Malicious attacks
  - during request methods CSRF , cross site request Forgery
