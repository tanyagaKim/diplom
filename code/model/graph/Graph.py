from model.graph.Mark import MarkedStatus
from model.graph.Transition import Transition


class Graph:
    def __init__(self, name, transitions, marked_statuses):
        self.name = name
        self.statuses = dict()
        self.matrix = dict()
        self.adjacency_list = dict()

        self.matrix_filling(transitions)
        self.marks_filling(marked_statuses)
        self.lists_filling(transitions)

    def matrix_filling(self, transitions):
        for transit in transitions:
            if isinstance(transit, Transition):
                if list(self.statuses.keys()).count(transit.status) == 0:
                    self.statuses.update({transit.status: None})
                    self.matrix.update({transit.status: dict.fromkeys(self.statuses.keys())})

                if list(self.statuses.keys()).count(transit.next_status) == 0:
                    self.statuses.update({transit.next_status: None})
                    self.matrix.update({transit.next_status: dict.fromkeys(self.statuses.keys())})

                for row in self.matrix.keys():
                    columns = list(self.matrix.get(row).keys())

                    if columns.count(transit.status) == 0:
                        self.matrix.get(row).update({transit.status: None})

                    if columns.count(transit.next_status) == 0:
                        self.matrix.get(row).update({transit.next_status: None})

                row = self.matrix.get(transit.status)
                row.update({transit.next_status: transit.options})

    def marks_filling(self, marked_statuses):
        for marked_status in marked_statuses:
            if isinstance(marked_status, MarkedStatus):
                self.statuses.update({marked_status.status: marked_status.mark})

    def lists_filling(self, transitions):
        for transit in transitions:
            if isinstance(transit, Transition):
                if list(self.adjacency_list.keys()).count(transit.status) == 0:
                    self.adjacency_list.update({transit.status: dict()})
                self.adjacency_list.get(transit.status).update({transit.next_status: transit.options})
