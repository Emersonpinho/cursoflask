from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

# Modelagem
    # Produto (id, name, price, description)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False) # 9 != 8.99
    description = db.Column(db.Text, nullable=True) # texto longo e opcional

@app.route('/api/products/add', methods=['POST'])
def add_product():
    # Recupera os dados enviados no corpo da requisição
    data = request.json

    # Verifica se os dados foram enviados corretamente e logo depois faz o retorno da resposta
    if 'name' in data and 'price' in data:
        product =  Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "product added successfully"}), 200
    return jsonify({"message": "invalid product data"}), 400

@app.route('/api/products/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product =  Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    return jsonify({"message": "Product not found"}), 404

@app.route('/api/products/<int:product id>', methods=['GET'])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "decription": product.description
        })

# Definir uma rota raiz (pagina incial) e a função que será executada ao requisitar.
@app.route('/')
def hello_world():
    return 'Hello, world!'

if __name__ == "__main__":
    app.run(debug=True)