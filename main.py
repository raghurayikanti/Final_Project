
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Optional

app = FastAPI()

# -------------------- Database Configuration --------------------
DB_FILE = "db.sqlite"

# -------------------- Utility Function --------------------
def execute_query(query: str, params: tuple = (), fetchone: bool = False, fetchall: bool = False):
    """Helper function to execute queries and handle database connections."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        if fetchone:
            return cursor.fetchone()
        if fetchall:
            return cursor.fetchall()
        return cursor.lastrowid

# -------------------- Pydantic Models --------------------
class Customer(BaseModel):
    name: str
    phone: str


class Item(BaseModel):
    name: str
    price: float


class Order(BaseModel):
    customer_id: int
    items: List[Item]
    notes: Optional[str] = None


# -------------------- Reusable Helpers --------------------
def check_record_exists(table: str, record_id: int):
    """Helper function to check if a record exists in a table."""
    query = f"SELECT * FROM {table} WHERE id = ?"
    return execute_query(query, (record_id,), fetchone=True)

# -------------------- Customer Endpoints --------------------
@app.post("/customers")
def create_customer(customer: Customer):
    try:
        query = "INSERT INTO customers (name, phone) VALUES (?, ?)"
        customer_id = execute_query(query, (customer.name, customer.phone))
        return {"id": customer_id, "message": "Customer created successfully."}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Customer with this phone already exists.")


@app.get("/customers/{id}")
def get_customer(id: int):
    customer = check_record_exists("customers", id)
    if customer:
        return {"id": customer[0], "name": customer[1], "phone": customer[2]}
    raise HTTPException(status_code=404, detail="Customer not found.")


@app.put("/customers/{id}")
def update_customer(id: int, customer: Customer):
    if not check_record_exists("customers", id):
        raise HTTPException(status_code=404, detail="Customer not found.")

    query = "UPDATE customers SET name = ?, phone = ? WHERE id = ?"
    execute_query(query, (customer.name, customer.phone, id))
    return {"message": "Customer updated successfully."}


@app.delete("/customers/{id}")
def delete_customer(id: int):
    if not check_record_exists("customers", id):
        raise HTTPException(status_code=404, detail="Customer not found.")

    query = "DELETE FROM customers WHERE id = ?"
    execute_query(query, (id,))
    return {"message": "Customer deleted successfully."}


# -------------------- Item Endpoints --------------------
@app.post("/items")
def create_item(item: Item):
    query = "INSERT INTO items (name, price) VALUES (?, ?)"
    item_id = execute_query(query, (item.name, item.price))
    return {"id": item_id, "message": "Item created successfully."}


@app.get("/items/{id}")
def get_item(id: int):
    item = check_record_exists("items", id)
    if item:
        return {"id": item[0], "name": item[1], "price": item[2]}
    raise HTTPException(status_code=404, detail="Item not found.")


@app.put("/items/{id}")
def update_item(id: int, item: Item):
    if not check_record_exists("items", id):
        raise HTTPException(status_code=404, detail="Item not found.")

    query = "UPDATE items SET name = ?, price = ? WHERE id = ?"
    execute_query(query, (item.name, item.price, id))
    return {"message": "Item updated successfully."}


@app.delete("/items/{id}")
def delete_item(id: int):
    if not check_record_exists("items", id):
        raise HTTPException(status_code=404, detail="Item not found.")

    query = "DELETE FROM items WHERE id = ?"
    execute_query(query, (id,))
    return {"message": "Item deleted successfully."}


# -------------------- Order Endpoints --------------------
@app.post("/orders")
def create_order(order: Order):
    # Check if customer exists
    if not check_record_exists("customers", order.customer_id):
        raise HTTPException(status_code=404, detail="Customer not found.")

    # Create the order
    query = "INSERT INTO orders (customer_id, notes, timestamp) VALUES (?, ?, strftime('%s', 'now'))"
    order_id = execute_query(query, (order.customer_id, order.notes or ""))

    # Handle items
    price_adjustments = []
    for item in order.items:
        item_data = execute_query("SELECT id, price FROM items WHERE name = ?", (item.name,), fetchone=True)
        if not item_data:
            raise HTTPException(status_code=404, detail=f"Item '{item.name}' not found.")
        
        item_id, correct_price = item_data
        if item.price != correct_price:
            price_adjustments.append(f"Item '{item.name}' price updated from {item.price} to {correct_price}.")
        execute_query("INSERT INTO order_items (order_id, item_id) VALUES (?, ?)", (order_id, item_id))

    response = {"id": order_id, "message": "Order created successfully."}
    if price_adjustments:
        response["price_adjustments"] = price_adjustments
    return response


@app.get("/orders/{id}")
def get_order(id: int):
    order = execute_query("SELECT id, customer_id, notes FROM orders WHERE id = ?", (id,), fetchone=True)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")

    items = execute_query(
        "SELECT i.name, i.price FROM order_items oi JOIN items i ON oi.item_id = i.id WHERE oi.order_id = ?",
        (id,),
        fetchall=True,
    )
    return {
        "id": order[0],
        "customer_id": order[1],
        "notes": order[2],
        "items": [{"name": item[0], "price": item[1]} for item in items],
    }

@app.put("/orders/{id}")
def update_order(id: int, order: Order):
    # Verify the order exists
    if not check_record_exists("orders", id):
        raise HTTPException(status_code=404, detail="Order not found.")

    # Update order notes and customer_id
    query = "UPDATE orders SET customer_id = ?, notes = ? WHERE id = ?"
    execute_query(query, (order.customer_id, order.notes or "", id))

    # Remove existing order items and replace with the new ones
    execute_query("DELETE FROM order_items WHERE order_id = ?", (id,))

    price_adjustments = []
    for item in order.items:
        item_data = execute_query("SELECT id, price FROM items WHERE name = ?", (item.name,), fetchone=True)
        if not item_data:
            raise HTTPException(status_code=404, detail=f"Item '{item.name}' not found.")

        item_id, correct_price = item_data
        if item.price != correct_price:
            price_adjustments.append(f"Item '{item.name}' price updated from {item.price} to {correct_price}.")
        execute_query("INSERT INTO order_items (order_id, item_id) VALUES (?, ?)", (id, item_id))

    response = {"id": id, "message": "Order updated successfully."}
    if price_adjustments:
        response["price_adjustments"] = price_adjustments
    return response

@app.delete("/orders/{id}")
def delete_order(id: int):
    if not check_record_exists("orders", id):
        raise HTTPException(status_code=404, detail="Order not found.")
    execute_query("DELETE FROM orders WHERE id = ?", (id,))
    return {"message": "Order deleted successfully."}
