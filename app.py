from flask import Flask

app = Flask(__name__)

# definir uma rota raiz (pagina incial) e a função que será executada ao requisitar.
@app.route('/')