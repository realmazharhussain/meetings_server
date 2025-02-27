from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import auth, rooms, bookings, docs
    app.register_blueprint(auth.bp)
    app.register_blueprint(rooms.bp)
    app.register_blueprint(bookings.bp)
    app.register_blueprint(docs.bp)

    @app.route('/')
    def home():
        return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Meeting Room Booking API</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    max-width: 800px;
                    margin: 40px auto;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                    border-bottom: 2px solid #eee;
                    padding-bottom: 10px;
                }
                .api-link {
                    color: #0066cc;
                    text-decoration: none;
                }
                .api-link:hover {
                    text-decoration: underline;
                }
                .endpoints {
                    margin-top: 20px;
                    padding: 15px;
                    background: #f5f5f5;
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <h1>Meeting Room Booking API</h1>
            <p>This is an API server for the Meeting Room Booking application. To use this service, please access it through a client application.</p>
            <div class="endpoints">
                <h2>Quick Links:</h2>
                <ul>
                    <li><a class="api-link" href="/rooms">View Available Rooms</a></li>
                    <li><a class="api-link" href="/docs/api.rst">API Documentation</a></li>
                </ul>
            </div>
        </body>
        </html>
        '''

    return app