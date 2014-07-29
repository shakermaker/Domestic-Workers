from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/')
def home():

    input = request.args.get('pay-rate', 'day')
    try:
        input2 = int(request.args.get('pay-amount', '0'))
    except ValueError:
        input2 = 0
    try:
        input3 = int(request.args.get('household-size', '1'))
    except ValueError:
        input3 = 1

    return render_template('index.html', input_variable=input, input2_variable=input2, input3_variable=input3)

if __name__ == '__main__':
    app.debug = True
    app.run()
