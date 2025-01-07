from app import create_app
from app import routes

app = create_app()

if __name__ == "__main__":
    routes.setup(app)
    app.run(debug=True)
