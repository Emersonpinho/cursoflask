from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY DATABASE URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

# Modelagem
# Produto (id, name, price, description)

class Product(db.Model):
    

# Definir uma rota raiz (pagina incial) e a função que será executada ao requisitar.
@app.route('/')
def hello_world():
    return 'Hello, world!'

if __name__ == "__main__":
    app.run(debug=True)