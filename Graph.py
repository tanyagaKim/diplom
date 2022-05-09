from model.graph.TransitionMatrix import TransitionMatrix


class Graph:
    def __init__(self, name, transitions):
        self.name = name
        self.matrix = TransitionMatrix().matrix_filling(transitions)
