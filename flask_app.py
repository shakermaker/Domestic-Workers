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

    input = request.args.get('pay-rate', 'day')
    input2 = int(request.args.get('pay-amount', '0'))
    input3 = int(request.args.get('household-size', '1'))

    minwage=1880
    payrate=0
    
    #Assumption using DoL info - a month includes 4.33 weeks and a week is for 6 work days.

    if input=="per day":
        payrate=input2*6*4.33
    elif input=="per week":
        payrate=input2*4.33
    elif input=="per month":
        payrate=input2

    minwage_ratio=payrate/minwage

    #Per person costs for each expenditure type
    #All costs are adjustable.

    #Proportional costs to start with
    rent_cost=1000
    food_cost=900
    trans_daily=30
    educ_cost=100
    comm_cost=100
    health_cost=50
    recreation_cost=100
    other_cost=200
    trans_cost=trans_daily*26
    
    totalcost=rent_cost+ input3*food_cost+trans_cost+educ_cost*(input3-2) + comm_cost*input3 + health_cost*input3 + other_cost + recreation_cost*input3

    final_output=payrate/totalcost*100

    if final_output>0 and final_output<=75:
        statement="You're paying too little given the living costs and the size of your household employee. Take time to reassess how much you're paying by using our tool."
    elif final_output>75 and final_output<=90:
        statement="You're nearly there! Take time to reassess the wage by using our tool or discussing costs with your household employee."
    elif final_output>90 and final_output<=100:
        statement="You're very close to paying a fair wage given the living costs and your employee's household size. Share your results!"
    elif final_output==0:
        statement="Try out the fair wage tool and see how your pay reflects living costs in South Africa."
    else:
        statement="This seems like a fair wage! Share your results!"

   #tmp = float(dataset[input2][input])

    return render_template('bootstrap.html', input_variable=input, input2_variable=input2, input3_variable=input3, output_variable=final_output, output_statement=statement)

if __name__ == '__main__':
    app.debug = True
    app.run()
