import csv
import matplotlib.pyplot as plt


with open('data/inputs.csv', 'r') as file:
    inputs = csv.DictReader(file)
    steer = [int(x['steer']) for x in inputs]
    #print(steer)
    plt.hist(steer, 50)
    plt.show()
