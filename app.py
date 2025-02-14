from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.login_view = 'login'
CORS(app)

# Modelagem
# usuario (id, username, password)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=True)

@app.route('/login', methods=["POST"])
def login():
    data = request.json
    
    user = User.query.filter_by(username=data.get("username")).first()
    
    if user and data.get("password") == user.password:
            login_user(user)
            return jsonify({"message": "logged in sucessfully"}), 200
    
    return jsonify({"message": "Unauthorized. Invalid credentials"}), 401
        


    
# Modelagem
# Produto (id, name, price, description)

#salvando no banco de dados
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
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
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

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "decription": product.description
        })
    return jsonify({"message": "product not found"}), 404

@app.route('/api/products/update/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "product not found"}), 404
    
    data = request.json
    if 'name' in data:
        product.name = data['name']

    if 'price' in data:
        product.price = data['price']

    if 'description' in data:
        product.description = data['description']

    db.session.commit()
    return jsonify({"message": "product updated successfully"}), 200

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price
        }
        product_list.append(product_data)

    return jsonify(product_list)

# Definir uma rota raiz (pagina incial) e a função que será executada ao requisitar.
@app.route('/')
def hello_world():
    return 'Hello, world!'

if __name__ == "__main__":
    app.run(debug=True)