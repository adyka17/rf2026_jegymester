from apiflask import APIFlask
from config import Config
from app.extensions import db


def create_app(config_class=Config):
    app = APIFlask(__name__, docs_path='/docs')
    app.config.from_object(config_class)

    app.config['API_TITLE'] = 'Jegymester API'
    app.config['API_VERSION'] = '0.1.0'
    app.config['OPENAPI_VERSION'] = '3.0.3'

    db.init_app(app)

    from flask_migrate import Migrate
    migrate = Migrate(app, db, render_as_batch=True)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.blueprints import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app