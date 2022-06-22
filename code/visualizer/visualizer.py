from pyvis.network import Network


class Visualizer:

    def __init__(self):
        self.net = Network(notebook=True, directed=True)

    def show_graph(self, graph):

        i = 0
        for status, next_status in graph.adjacency_list.items():
            self.net.add_node(i, label=status)
            self.net.add_node(i + 1, label=next_status)
            i += 2
        #self.net.show("mygraph.html")

    def show_model(self, model):
        for graph in model.schemes:
            self.show_graph(graph)
        #self.net.show('basic.html')
