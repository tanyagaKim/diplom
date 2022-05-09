from model.graph.Graph import Graph
from model.graph.information_model.Transition import Transition


class Model:
    def __init__(self):
        self.name = "GraphModel"
        self.schemes = list()

    def add_graph(self, name, strings):
        transitions = []

        for string in strings:

            argv = string.split()
            status, next_status = argv[0], argv[1]
            argv = argv[2:]

            options = []

            for arg in argv:
                options.append(Option(arg))

            transitions.append(Transition(status, next_status, options))

        self.schemes.append(Graph(name, transitions))

    def delete_graph(self, name):
        for graph in self.schemes:
            if graph.name == name:
                self.schemes.remove(graph)
                break
