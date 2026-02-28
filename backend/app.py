from flask import Flask
from flask_cors import CORS
from routes.cnpj_routes import cnpj_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(cnpj_bp, url_prefix='/api/cnpj')

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True, port=5000)