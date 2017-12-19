from Neuron import *
from Synapse import *
import csv
import datetime
import os

# Create timestamp for folder containing neuron spike traces
folder_name = '{:%Y-%m-%d %H-%M-%S}'.format(datetime.datetime.now())
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Open .csv file containing connection weights and read into a list
with open('testdata.csv', newline='') as weighttable:
    reader = csv.reader(weighttable, delimiter=',', quotechar='|')
    weight_table = list(reader)

# Create the list of neurons based on the size of the weight table
neurons = []
for i in range(0, len(weight_table)):
    neurons.append(Neuron(folder_name, i))

# Create table of synapse objects using the weight table
synapse_table = []
for i in range(0, len(weight_table)):
    synapse_table.append([])
    for j in range(0, len(weight_table)):
        synapse_table[i].append(Synapse(neurons[i], neurons[j], float(weight_table[i][j])))

for i in range(0, len(synapse_table)):
    for j in range(0, len(synapse_table)):
        synapse_table[i][j].add_complimentary_synapse(synapse_table[j][i])


# Loop to run the simulation, every loop increments time by 1
time = 0
for p in range(1000):
    time += 1
    neurons[1].fire(synapse_table, neurons, time)  # Manually fire one neuron as much as possible (just to give some input)

    # Queue up all the neurons that need to fire
    to_fire = []
    for i in range(len(neurons)):
        if(neurons[i].potential > neurons[i].trigger_threshold):
            to_fire.append(neurons[i])
    # Fire all the neurons in the queue
    for i in range(len(to_fire)):
        to_fire[i].fire(synapse_table, neurons, time)


# Write output files
# Create .csv file containing the resulting weights
with open(folder_name + '/resulting_weights.csv', 'w') as f:
    for i in range(0, len(synapse_table)):
        for j in range(0, len(synapse_table)):
            f.write(str(synapse_table[i][j].weight))
            f.write(",")
        f.write('\n')
# Create .csv file containing the overall change in weights
with open(folder_name + '/resulting_deltas.csv', 'w') as f:
    for i in range(0, len(synapse_table)):
        for j in range(0, len(synapse_table)):
            f.write(str(synapse_table[i][j].weight - float(weight_table[i][j])))
            f.write(",")
        f.write('\n')
