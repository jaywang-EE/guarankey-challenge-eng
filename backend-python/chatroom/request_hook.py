from app import app
from flask_wtf.csrf import generate_csrf

@app.after_request
def after_request(response):
    csrf_token = generate_csrf()
    response.set_cookie("csrf_token", csrf_token)
    return response