import os


class Neuron:
    def __init__(self, folder_name, index):
        self.folder_name = folder_name  # Folder to index the spike traces into
        self.index = index  # Index of this neuron
        self.potential = 0  # Current potential, caused by being acted on by a synapse
        self.trigger_threshold = 100  # The neuron will fire after the potential reaches this threshold
        self.refractory_period = 5  # Time in "ticks" that the neuron is in refractory and cannot gain potential
        self.last_fire = -1000  # Time since this neuron last fired, initialized to a large negative to represent having never fired

    def add_potential(self, weight):  # Rule for updating potentials
        magnitude = 10  # the largest possible update in potential for a single firing
        added_potential = weight * magnitude  # produces updates in potential in range [0, magnitude]
        self.potential += added_potential
        return

    def fire(self, synapse_table, neurons, time):
        self.potential = 0
        if time - self.last_fire > self.refractory_period:
            # Apply weight to all neurons
            for i in range(0, len(synapse_table)):
                synapse = synapse_table[self.index][i]
                if time - synapse.target_neuron.last_fire > synapse.target_neuron.refractory_period and synapse.weight != 1:  # if the target neuron is not in refractory
                    synapse.target_neuron.add_potential(synapse.weight)  # call add potential on the target neuron

            # Update weights of Neurons that fired in the past
            for i in range(0, len(synapse_table)):
                synapse = synapse_table[i][self.index]
                synapse.adjust_weights(time - synapse.source_neuron.last_fire)

            # Update neuron spike trace file
            file_name = "Neuron " + str(self.index)
            self.last_fire = time
            file_path = self.folder_name + "/" + file_name
            with open(file_path, 'a') as file:
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    file.write("," + str(time))
                else:
                    file.write(str(time))















