from website import create_app
from flask_mail import Mail

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) # Set to false in production