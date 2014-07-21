from flask import Flask, request, render_template
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

    input = request.args.get('input-variable', 'Daily')
    input2 = int(request.args.get('input2-variable', '0'))
    input3 = int(request.args.get('input3-variable', '1'))

    minwage=1880
    payrate=0

    #Assumption using DoL info - a month includes 4.33 weeks and a week is for 6 work days.

    if input=="day":
        payrate=input2*6*4.33
    elif input=="week":
        payrate=input2*4.33
    elif input=="month":
        payrate=input2

    minwage_ratio=payrate/minwage

    #Per person costs for each expenditure type
    #All costs are adjustable.

    #Proportional costs to start with
    food_wgt=0.45

    rent_cost=1000
    food_cost=900
    trans_daily=30
    educ_cost=100
    comm_cost=100
    health_cost=50
    other_cost=200
    
    trans_cost=trans_daily*26
    
    totalcost=rent_cost+ input3*food_cost+trans_cost+educ_cost*2 + comm_cost*input3 + health_cost*input3 + other_cost*2

    final_output=payrate/totalcost*100



    #tmp = float(dataset[input2][input])

    return render_template('bootstrap.html', input_variable=input, input2_variable=input2, input3_variable=input3, output_variable=final_output)

if __name__ == '__main__':
    app.debug = True
    app.run()
