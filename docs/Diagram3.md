sequenceDiagram
    actor User
    participant Browser
    participant Flask
    participant Auth
    participant Products
    participant Cart
    participant Orders
    participant Database
    participant Payment

    User->>Browser: Visit marketplace
    Browser->>Flask: GET /
    Flask->>Browser: Render home page

    %% Registration flow
    User->>Browser: Click Register
    Browser->>Flask: GET /auth/register
    Flask->>Auth: Route to register page
    Auth->>Browser: Render registration form
    User->>Browser: Fill registration form
    Browser->>Flask: POST /auth/register
    Flask->>Auth: Process registration
    Auth->>Database: Create new user
    Database-->>Auth: Confirm creation
    Auth->>Browser: Redirect to login

    %% Login flow
    User->>Browser: Fill login form
    Browser->>Flask: POST /auth/login
    Flask->>Auth: Authenticate user
    Auth->>Database: Verify credentials
    Database-->>Auth: Return user data
    Auth->>Browser: Set session cookie
    Auth->>Browser: Redirect to home

    %% Browse products
    User->>Browser: Click Browse Products
    Browser->>Flask: GET /products
    Flask->>Products: Route to products
    Products->>Database: Query products
    Database-->>Products: Return product list
    Products->>Browser: Render products page

    %% Add to cart
    User->>Browser: Click Add to Cart
    Browser->>Flask: POST /cart/add
    Flask->>Cart: Process add to cart
    Cart->>Database: Add item to cart
    Database-->>Cart: Confirm addition
    Cart->>Browser: Update cart display

    %% Checkout process
    User->>Browser: Click Checkout
    Browser->>Flask: GET /orders/checkout
    Flask->>Orders: Route to checkout
    Orders->>Database: Get cart items
    Database-->>Orders: Return cart data
    Orders->>Browser: Render checkout page
    User->>Browser: Confirm order
    Browser->>Flask: POST /orders/create
    Flask->>Orders: Process order creation
    Orders->>Payment: Initialize payment
    Payment-->>Orders: Return payment session
    Orders->>Database: Create order record
    Database-->>Orders: Confirm creation
    Orders->>Browser: Redirect to payment
    User->>Browser: Complete payment
    Browser->>Flask: GET /orders/success
    Flask->>Orders: Process payment success
    Orders->>Database: Update order status
    Database-->>Orders: Confirm update
    Orders->>Browser: Render success page
