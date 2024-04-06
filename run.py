from app import create_app
from Logging import logger

from app.routes.auth_routes import auth_routes
from app.routes.manager_routes import manager_routes
from app.routes.user_routes import user_routes

app = create_app()

app.register_blueprint(auth_routes)
app.register_blueprint(manager_routes)
app.register_blueprint(user_routes)

if __name__ == '__main__':
    try:
        app.run(debug=True, host='127.0.0.1', port=5001)
    except Exception as e:
        logger.exception(f"Error while hosting the app : {e}")
