import logging

from flask import Flask
from config import Config

logging.basicConfig(filename='logs.log', level=logging.INFO, format=f'%(asctime)s %(levelname)s : %(message)s')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    app.logger.setLevel(logging.INFO)
    app.logger.info('Victiv Test App')

    return app