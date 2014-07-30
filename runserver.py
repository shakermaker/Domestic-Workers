from app.flask_app import app

if __name__ == "__main__":
    # run Flask dev-server
    app.debug = True
    app.run(port=5000)