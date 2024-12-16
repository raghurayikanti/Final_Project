# **REST API backend for dosa restaurant **

This project is to use an SQLite database and FastAPI to provide access to three objects: customers, items, and orders.** for the backend and **SQLite** as the database.

---

## **Features**

- **Customer Management**
  - Create, read, update, and delete customers.
- **Menu Item Management**
  - Add, retrieve, update, and delete menu items.
- **Order Management**
  - Create, retrieve, update, and delete orders.
  - Orders can contain multiple items.

---

## **Technologies Used**

- **FastAPI**: Framework for building the RESTful API.
- **SQLite**: Lightweight database to store customers, menu items, and orders.
- **Pydantic**: Data validation for API request bodies.
- **SQLAlchemy** (Optional): For ORM-based data handling (if needed).

---
## **API Endpoints**

### **Customer Endpoints**

- **POST `/customers`**: Create a new customer.
  - **Request Body**: 
    ```json
    {
      "name": "Customer Name",
      "phone": "Customer Phone"
    }
    ```
  - **Response**: 
    ```json
    {
      "id": 1,
      "message": "Customer created successfully."
    }
    ```

- **GET `/customers/{id}`**: Retrieve customer details by ID.
  - **Response**: 
    ```json
    {
      "id": 1,
      "name": "Customer Name",
      "phone": "Customer Phone"
    }
    ```

- **PUT `/customers/{id}`**: Update customer details.
  - **Request Body**:
    ```json
    {
      "name": "Updated Name",
      "phone": "Updated Phone"
    }
    ```
  - **Response**:
    ```json
    {
      "message": "Customer updated successfully."
    }
    ```

- **DELETE `/customers/{id}`**: Delete a customer.
  - **Response**:
    ```json
    {
      "message": "Customer deleted successfully."
    }
    ```

---

### **Item Endpoints**

- **POST `/items`**: Add a new item to the menu.
  - **Request Body**: 
    ```json
    {
      "name": "Item Name",
      "price": 12.99
    }
    ```
  - **Response**: 
    ```json
    {
      "id": 1,
      "message": "Item created successfully."
    }
    ```

- **GET `/items/{id}`**: Get item details by ID.
  - **Response**: 
    ```json
    {
      "id": 1,
      "name": "Item Name",
      "price": 12.99
    }
    ```

- **PUT `/items/{id}`**: Update an existing item in the menu.
  - **Request Body**:
    ```json
    {
      "name": "Updated Item Name",
      "price": 15.99
    }
    ```
  - **Response**: 
    ```json
    {
      "message": "Item updated successfully."
    }
    ```

- **DELETE `/items/{id}`**: Delete an item from the menu.
  - **Response**:
    ```json
    {
      "message": "Item deleted successfully."
    }
    ```

---

### **Order Endpoints**

- **POST `/orders`**: Create a new order for a customer with one or more items.
  - **Request Body**:
    ```json
    {
      "customer_id": 1,
      "items": [
        {
          "name": "Pizza",
          "price": 12.99
        },
        {
          "name": "Burger",
          "price": 8.99
        }
      ],
      "notes": "Extra cheese on pizza."
    }
    ```
  - **Response**: 
    ```json
    {
      "id": 1,
      "message": "Order created successfully.",
      "price_adjustments": ["Item 'Pizza' price adjusted from 10.99 to 12.99."]
    }
    ```

- **GET `/orders/{id}`**: Get order details, including items.
  - **Response**:
    ```json
    {
      "id": 1,
      "customer_id": 1,
      "notes": "Extra cheese on pizza.",
      "items": [
        {
          "name": "Pizza",
          "price": 12.99
        },
        {
          "name": "Burger",
          "price": 8.99
        }
      ]
    }
    ```

- **PUT `/orders/{id}`**: Update an existing order.
  - **Request Body**:
    ```json
    {
      "customer_id": 1,
      "items": [
        {
          "name": "Pizza",
          "price": 12.99
        },
        {
          "name": "Pasta",
          "price": 10.99
        }
      ],
      "notes": "Changed to pasta."
    }
    ```
  - **Response**:
    ```json
    {
      "id": 1,
      "message": "Order updated successfully.",
      "price_adjustments": ["Item 'Burger' price adjusted from 8.99 to 10.99."]
    }
    ```

- **DELETE `/orders/{id}`**: Delete an order.
  - **Response**:
    ```json
    {
      "message": "Order deleted successfully."
    }
    ```

## **Installation**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/raghurayikanti/Final_Project/.git
   
   ```
2. **Set up a virtual environment** (optional but recommended):
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Initialize the database**:
Run the following command to create the database schema and tables.
```
python init_db.py
```
## **Running the Application**

1. **Start the FastAPI server**:
   Run the following command to start the FastAPI server. The server will be running in development mode with hot reload enabled.

   ```bash
   uvicorn main:app --reload
   ```
2. **The API will be accessible at http://127.0.0.1:8000.
   Access the Swagger UI: FastAPI provides an auto-generated interactive API documentation. To access it, go to:

   ```bash
   http://127.0.0.1:8000/docs
   ```









