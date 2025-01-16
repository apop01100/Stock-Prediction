from flask import Flask, redirect, request
from app.config import DevelopmentConfig, ProductionConfig
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

def create_app(test_config=None, production_config=os.getenv("PRODUCTION_CONFIG")):
    app = Flask(__name__)
    
    if test_config is not None:
        app.config.from_object(test_config)
        
    if production_config is not None:
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
        
    CORS(app)
    
    @app.route("/")
    def index():
        return redirect("/apidocs/#/")
    
    @app.before_request
    def handle_options():
        if request.method == 'OPTIONS':
            return '', 204
        
    from app.routes import lstm_models
    url_prefix = "/api/v1/"
    app.register_blueprint(lstm_models, url_prefix=url_prefix + "lstm")
    
    return app