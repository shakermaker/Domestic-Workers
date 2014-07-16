from flask import Flask, render_template
app = Flask(__name__)
import csv

def read_data(filename):
    """
    Read specified csv file, and return it as a list of dicts.
    """

    with open(filename, 'r') as f:
        return list(csv.DictReader(f))

dataset=read_data('Book1.csv')


@app.route('/')
def home():

    tmp = dataset[1]['food_wgt']
    
    return render_template('home.html', output_variable=tmp)

if __name__ == '__main__':
    app.debug = True
    app.run()
