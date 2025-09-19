#create Flask app, load config
import os
from flask import Flask
from .config import Config
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS


load_dotenv()


jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    # load configuration
    
    app.config.from_object(Config)
    
    # Set JWT secret key
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")  
    app.config["PROPAGATE_EXCEPTIONS"] = True
    jwt.init_app(app)
    
    
    #import and register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp  
    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(user_bp, url_prefix="/user")
    
    
    # Initialize extensions here (like CORS, JWT later)
    # CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"])

     # ✅ ALLOW Netlify domain
    CORS(app, resources={r"/*": {"origins": [
        "https://basicuseraccessmanagement.netlify.app",
        "http://localhost:5173"  # (for local dev)
    ]}}, supports_credentials=True)
    # jwt = JWTManager()
    # jwt.init_app(app)  
    
    # @app.route("/")
    # def index():
    #     return "Flask app is running!"
    # # Register blueprints
    # # app.register_blueprint()
    # print("Loaded config:", app.config["SECRET_KEY"][:5], "...")  

    return app



# Testing
if __name__ == "__main__":
    app = create_app()
    app.run(debug = True)
