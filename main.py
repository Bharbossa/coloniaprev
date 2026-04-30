from firebase_functions import https_fn
from app import create_app

app = create_app()

@https_fn.on_request()
def flask_app(req: https_fn.Request) -> https_fn.Response:
    # Set the environment variable for SQLite just in case
    import os
    os.environ['USE_SQLITE'] = 'True'
    
    with app.request_context(req.environ):
        return app.full_dispatch_request()
