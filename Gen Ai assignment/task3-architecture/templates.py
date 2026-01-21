TEMPLATES = {
    "chatbot": {
        "modules": [
            "Frontend UI",
            "Chat Controller",
            "AI Response Engine",
            "Database Layer"
        ],
        "apis": [
            "POST /chat",
            "GET /chat/history"
        ],
        "database": [
            "Users(id, name, email)",
            "Messages(id, user_id, message, response, timestamp)"
        ],
        "pseudocode": [
            "Receive user message",
            "Send message to AI engine",
            "Store response in database",
            "Return response to UI"
        ]
    },

    "ecommerce": {
        "modules": [
            "Product Service",
            "Order Service",
            "Payment Service",
            "User Service"
        ],
        "apis": [
            "GET /products",
            "POST /order",
            "POST /payment"
        ],
        "database": [
            "Products(id, name, price)",
            "Orders(id, user_id, total)",
            "Payments(id, order_id, status)"
        ],
        "pseudocode": [
            "Fetch product list",
            "Create order",
            "Process payment",
            "Confirm order"
        ]
    }
}
