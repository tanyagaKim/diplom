from model.graph.Graph import Graph
from model.graph.Mark import MarkedStatus
from model.graph.Transition import Transition, GraphTransition
from model.graph.information_model.Option import Option


class Model:
    def __init__(self, name='GraphModel'):
        self.name = name
        self.schemes = list()
        self.graph_transition_list = list()
        self.graph_matrix = dict()

    def add_graph(self, name, list_transitions, list_marked_statuses):
        transitions = []

        for string in list_transitions:
            argv = string.split()
            status, next_status = argv[0], argv[1]
            argv = argv[2:]

            options = []

            for arg in argv:
                command, parameters = arg.split(':')
                options.append(Option(command, parameters))

            transitions.append(Transition(status, next_status, options))

        marked_statuses = []

        for marked_status in list_marked_statuses:
            argv = marked_status.split()
            mark, status = argv[0], argv[1]

            marked_statuses.append(MarkedStatus(mark, status))

        self.schemes.append(Graph(name, transitions, marked_statuses))
        self._graph_matrix_filling([GraphTransition(name, transition.status, name, transition.next_status, 
                                                    transition.options) for transition in transitions])

    def delete_graph(self, name):
        for graph in self.schemes:
            if graph.name == name:
                self.schemes.remove(graph)
                break

    def add_graph_transition(self, string):
        argv = string.split()
        graph, status, next_graph, next_status = argv[0], argv[1], argv[2], argv[3]
        argv = argv[4:]

        options = []

        for arg in argv:
            command, parameters = arg.split(':')
            options.append(Option(command, parameters))

        if self._check_graph_name(graph) and self._check_graph_name(graph):
            self.graph_transition_list.append(GraphTransition(graph, status, next_graph, next_status, options))
            self._graph_matrix_filling([GraphTransition(graph, status, next_graph, next_status, options)])

    def _graph_matrix_filling(self, graph_transitions):
        for graph_transition in graph_transitions:
            if isinstance(graph_transition, GraphTransition):
                initial = graph_transition.graph + graph_transition.status
                purpose = graph_transition.next_graph + graph_transition.next_status

                if list(self.graph_matrix.keys()).count(initial) == 0:
                    self.graph_matrix.update({initial: dict().fromkeys(self.graph_matrix.keys())})

                if list(self.graph_matrix.keys()).count(purpose) == 0:
                    self.graph_matrix.update({purpose: dict().fromkeys(self.graph_matrix.keys())})

                for row in self.graph_matrix.keys():
                    columns = list(self.graph_matrix.get(row))

                    if columns.count(initial) == 0:
                        self.graph_matrix.get(row).update({initial: None})

                    if columns.count(purpose) == 0:
                        self.graph_matrix.get(row).update({purpose: None})

                row = self.graph_matrix.get(initial)
                row.update({purpose: graph_transition.options})

    def _check_graph_name(self, name):
        for graph in self.schemes:
            if graph.name == name:
                return True
        return False
