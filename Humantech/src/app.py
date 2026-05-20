import logging

from flask import Flask
from config import Config
from extensions import mysql

from routes.auth import auth_bp
from routes.home import home_bp
from routes.juguetes import juguetes_bp
from routes.categorias import categorias_bp


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)

    mysql.init_app(app)

    logging.basicConfig(filename="app.log", level=logging.ERROR)

    @app.before_request
    def before_request():
        try:
            mysql.connection.ping()
        except Exception as e:
            print("Error de reconexión:", e)

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(juguetes_bp)
    app.register_blueprint(categorias_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001, threaded=True)
