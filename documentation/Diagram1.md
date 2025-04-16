graph TD
    User((Customer)) --> Home[Home Page]
    Home -->|Login| Login[Login Page]
    Home -->|Register| Register[Register Page]
    Register --> Login
    Login --> Home
    
    Home -->|Browse| Products[Products Page]
    Products -->|View| ProductDetail[Product Detail]
    ProductDetail -->|Add to Cart| Cart[Shopping Cart]
    Products -->|Add to Cart| Cart
    
    Cart -->|Continue Shopping| Products
    Cart -->|Checkout| Checkout[Checkout]
    Checkout -->|Pay| Payment[Payment]
    Payment -->|Complete| Confirmation[Order Confirmation]
    
    style User fill:#f9f,stroke:#333,stroke-width:2px
    style Home fill:#bbf,stroke:#333,stroke-width:1px
    style Login fill:#bbf,stroke:#333,stroke-width:1px
    style Register fill:#bbf,stroke:#333,stroke-width:1px
    style Products fill:#bbf,stroke:#333,stroke-width:1px
    style ProductDetail fill:#bbf,stroke:#333,stroke-width:1px
    style Cart fill:#bbf,stroke:#333,stroke-width:1px
    style Checkout fill:#bbf,stroke:#333,stroke-width:1px
    style Payment fill:#bbf,stroke:#333,stroke-width:1px
    style Confirmation fill:#bbf,stroke:#333,stroke-width:1px
