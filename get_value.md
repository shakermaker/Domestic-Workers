Domestic-Workers
================
import csv

def read_data():

	with open('Nids_w3.csv', 'r') as f:
		return list(csv.DictReader(f))

dataset=read_data()
		
print(dataset[1]['food_wgt'])
