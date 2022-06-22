class Transition:
    def __init__(self, status, next_status, options=None):
        self.status = str
        self.next_status = str
        self.options = list

        self.status = status
        self.next_status = next_status
        self.options = options


class GraphTransition(Transition):
    def __init__(self, graph, status, next_graph, next_status, options=None):
        super().__init__(status, next_status, options)

        self.graph = str
        self.next_graph = str

        self.graph = graph
        self.next_graph = next_graph
