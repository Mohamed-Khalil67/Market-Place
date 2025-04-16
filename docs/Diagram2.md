classDiagram
    class User {
        +id: Integer
        +username: String
        +email_address: String
        +password_hash: String
        +budget: Integer
        +items: Relationship
        +cart_items: Relationship
        +orders: Relationship
        +check_password_correction()
        +can_purchase()
        +can_sell()
    }
    
    class Item {
        +id: Integer
        +name: String
        +price: Integer
        +barcode: String
        +description: String
        +image_url: String
        +category_id: Integer
        +stock: Integer
        +created_at: DateTime
        +updated_at: DateTime
        +owner: Integer
        +buy()
        +sell()
    }
    
    class Category {
        +id: Integer
        +name: String
        +description: String
        +items: Relationship
    }
    
    class CartItem {
        +id: Integer
        +user_id: Integer
        +item_id: Integer
        +quantity: Integer
        +added_at: DateTime
        +item: Relationship
        +subtotal: Property
    }
    
    class Order {
        +id: Integer
        +user_id: Integer
        +status: String
        +total_amount: Integer
        +created_at: DateTime
        +payment_id: String
        +items: Relationship
        +user: Relationship
    }
    
    class OrderItem {
        +id: Integer
        +order_id: Integer
        +item_id: Integer
        +quantity: Integer
        +price: Integer
        +item: Relationship
    }
    
    User "1" -- "many" Item: owns
    User "1" -- "many" CartItem: has
    User "1" -- "many" Order: places
    Category "1" -- "many" Item: categorizes
    CartItem "many" -- "1" Item: contains
    Order "1" -- "many" OrderItem: includes
    OrderItem "many" -- "1" Item: references
