# Domestic-Workers
# ================
import csv


def read_data(filename):
    """
    Read specified csv file, and return it as a list of dicts.
    """

    with open(filename, 'r') as f:
        return list(csv.DictReader(f))

dataset=read_data('Nids_w3.csv')

print(dataset[1]['food_wgt'])
