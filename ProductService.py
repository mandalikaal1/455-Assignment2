import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tasks.sqlite')
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer)


# endpoint 1: get all products
@app.route('/products', methods=['GET'])
def get_tasks():
    tasks = Product.query.all()
    task_list = [{"id": task.id, "title": task.title, "done": task.done} for task in tasks]
    return jsonify({"tasks": task_list})


# Endpoint 2: Get a specific product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_task(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({"product": {"id": product.id, "name": product.name, "quantity": product.quantity}})
    else:
        return jsonify({"error": "Task not found"}), 404


# Endpoint 3: Create a new product
@app.route('/products', methods=['POST'])
def create_task():
    data = request.json
    if "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    new_product = Product(name=data['name'], done=False)
    db.session.add(new_product)
    db.session.commit()

    return jsonify(
        {"message": "Product created", "product": {"id": new_product.id,
                                                   "name": new_product.name, "quantity": new_product.quantity}}), 201


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
