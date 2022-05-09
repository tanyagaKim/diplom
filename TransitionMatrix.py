from model.graph.information_model.Transition import Transition


class TransitionMatrix:
    def __init__(self,):
        self.matrix = dict()

    def matrix_filling(self, transitions):

        for transit in transitions:
            if isinstance(transit, Transition):
                pair = dict([transit.next_status, transit.options])
                self.matrix.update([transit.status, pair])
