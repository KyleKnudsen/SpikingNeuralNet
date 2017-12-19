class Synapse:
    def __init__(self, source_neuron, target_neuron, weight):
        self.source_neuron = source_neuron
        self.target_neuron = target_neuron
        self.weight = weight
        self.complimentary_synapse = None

    def add_complimentary_synapse(self, synapse):
        self.complimentary_synapse = synapse

    # time is time since synapse was last triggered
    def adjust_weights(self, time):
        adjustment_period = 100
        if time < adjustment_period:
            if self.weight != 0 or 1:
                self.weight += ((adjustment_period - time) / adjustment_period) * (1 - self.weight) / 10
            if self.complimentary_synapse.weight != 0 or 1:
                self.complimentary_synapse.weight -= ((adjustment_period - time) / adjustment_period) * (self.complimentary_synapse.weight /10)

    """
    # time is time since complimentary synapse was last triggered
    def punish(self, time, rewarded_synapse):
        if time <= rewarded_synapse.reward_period:
            self.weight = self.weight - ((rewarded_synapse.reward_period - time) / rewarded_synapse.reward_period) * rewarded_synapse.reward_magnitude
    """