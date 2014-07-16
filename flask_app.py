from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    
    return '<h1>Minimum Wage: The Fictional Increase</h1>'

if __name__ == '__main__':
    app.run()
