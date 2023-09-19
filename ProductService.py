import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
products = [
    {"id": 1, "name": "tomatoes", "quantity": 100, "price": 2.36},
    {"id": 2, "name": "dish soap", "quantity": 50, "price": 4.68},
    {"id": 3, "name": "detergent", "quantity": 75, "price": 10.12}
]


# endpoint 1: get all products
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({"products": products})


# Endpoint 2: Get a specific product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_specific_product(product_id):
    task = next((product for product in products if product["id"] == product_id), None)
    if task:
        return jsonify({"product": products})
    else:
        return jsonify({"error": "product not found"}), 404


# Endpoint 3: Create a new product
@app.route('/products', methods=['POST'])
def create_product():
    new_product = {
        "id": len(products) + 1,
        "name": request.json.get('name'),
        "quantity": request.json.get('quantity'),
        "price": request.json.get('price')
    }
    products.append(new_product)
    return jsonify({"message": "Product created", "product": new_product}), 201


if __name__ == '__main__':
    app.run(debug=True)
