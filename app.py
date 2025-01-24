from flask import Flask

app = Flask(__name__)

# definir uma rota raiz (pagina incial) e a função que será executada ao requisitar.
@app.route('/')
def hello_world():
    return 'Hello, world!'


app.run(debug=True)