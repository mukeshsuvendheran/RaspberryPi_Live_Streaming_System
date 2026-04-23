from flask_cors import CORS

def init_extensions(app):
    CORS(app)

    # Later you can add:
    # Mongo init
    # Redis
    # JWT config