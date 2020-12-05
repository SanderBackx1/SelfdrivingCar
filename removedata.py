import csv
import random

f = open('data/inputs2.csv', 'w')
with open('data/inputs.csv', 'r') as file:
    inputs = csv.DictReader(file)
    for row in inputs:
        if int(row['steer']) == 0:
            if random.randint(0, 10) > 8:
                f.write(f"{row['img_path']},{row['speed']},{row['steer']},{row['accel']},{row['brake']}\n")
        else:
            f.write(f"{row['img_path']},{row['speed']},{row['steer']},{row['accel']},{row['brake']}\n")
f.close()
