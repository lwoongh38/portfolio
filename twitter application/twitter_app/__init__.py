from flask import Flask
from twitter_app.routes import main_routes, add_routes, get_routes, delete_routes, update_routes, predict_routes
from twitter_app.models import db, migrate


DATABASE_URI = "sqlite:///twitter.sqlite3"

# factory pattern
def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_routes.main_routes) # '/' 
    app.register_blueprint(add_routes.add_routes, url_prefix='/add') # '/add'
    app.register_blueprint(get_routes.get_routes, url_prefix='/get') # '/get'
    app.register_blueprint(delete_routes.delete_routes, url_prefix='/delete') # '/delete'
    app.register_blueprint(update_routes.update_routes, url_prefix='/update') # '/update'
    app.register_blueprint(predict_routes.predict_routes, url_prefix='/predict') # '/predict'
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)