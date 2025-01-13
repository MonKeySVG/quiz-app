from flask import Flask
from app.models import initialize_database

def create_app(*args, **kwargs):
    """
    Crée et configure une instance de l'application Flask.
    """
    app = Flask(__name__)

    # Enregistrer les Blueprints
    from app.path.questions import bp as quiz_bp
    from app.path.participations import bp as participations_bp

    app.register_blueprint(quiz_bp, url_prefix='/')
    app.register_blueprint(participations_bp, url_prefix='/')

    # Initialiser la base de données si nécessaire
    with app.app_context():
        initialize_database()

    return app

