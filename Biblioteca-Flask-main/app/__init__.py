from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():

    app = Flask(__name__)    
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(idUser):
        from .models.users import User
        return User.query.get(int(idUser))

    # 🔥 IMPORTAR TODOS LOS MODELOS
    from .models.users import User
    from .models.authors import Author
    from .models.rooms import Room
    from .models.perfil import Perfil
    from .models.publicacion import Publicacion
    from .models.etiqueta import Etiqueta

    # 🔗 IMPORTAR BLUEPRINTS
    from app.routes import (
        auth, author_routes, users_route, 
        room_routes, users_route_async, perfil_route
    )
    from .routes.publicacion_route import bp as publicacion_bp

    # 🔗 REGISTRAR BLUEPRINTS
    app.register_blueprint(auth.bp)
    app.register_blueprint(author_routes.bp)
    app.register_blueprint(users_route.bp)
    app.register_blueprint(room_routes.bp)
    app.register_blueprint(users_route_async.bp)
    app.register_blueprint(perfil_route.bp)
    app.register_blueprint(publicacion_bp)  # 🔥 ESTA ES LA NUEVA

    @app.errorhandler(Exception)
    def handle_error(e):
        print(f"An error occurred: {str(e)}")
        return {"error": str(e)}, 500

    return app