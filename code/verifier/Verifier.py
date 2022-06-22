from model.Model import Model
import numpy as np

from model.graph.information_model.Command import AllCommand, AnyCommand


class MultiplicationMatrix:
    @staticmethod
    def direct_multiply(matrix_a, matrix_b):
        n = len(matrix_a)
        l1 = len(matrix_a[0])
        l2 = len(matrix_b)
        m = len(matrix_b[0])

        if l1 != l2:
            return IOError

        matrix_product = np.zeros((n, m), dtype="i").tolist()
        for row in range(0, n):
            for col in range(0, m):
                for k in range(0, l1):
                    matrix_product[row][col] = matrix_product[row][col] or matrix_a[row][k] * matrix_b[k][col]
        return matrix_product


class BaseVerifier:

    def __init__(self):
        self.warnings = list()
        self.errors = list()
        #self.successes = list()

    @staticmethod
    def _determinate_marked_statuses(dict_statuses, marker):
        marked_statuses = dict()
        i = 0

        for status, mark in dict_statuses.items():
            if mark == marker:
                marked_statuses.update({i: status})
            i += 1

        return marked_statuses

    def add_warning(self, graph_name, mark, status):
        self.warnings.append([graph_name, mark, status])

    def add_error(self, graph_name, mark, status):
        self.errors.append([graph_name, mark, status])

    def check_model(self, information_model):
        pass


class GraphMatrixVerifier(BaseVerifier):

    @staticmethod
    def _create_adjacency_matrix(graph_matrix):
        matrix = []

        for status, values in graph_matrix.items():
            row = []
            for next_status, options in values.items():
                if options is not None:
                    row.append(1)
                else:
                    row.append(0)
            matrix.append(row)

        return matrix

    def _verify_start_graph(self, graph_name, start_status_dict, status_dict, steps):
        result = True

        for start_index, start in start_status_dict.items():
            for step_matrix in steps:
                for i in range(len(status_dict)):
                    if step_matrix[i][start_index] == 1:  # найден переход в начальный статус
                        self.add_error(graph_name, 'start',  start, status_dict[i])
                        result = False

        return result

    def _verify_end_graph(self, graph_name, end_status_dict, status_dict, steps):
        result = True

        for i in range(len(status_dict)):
            if end_status_dict.get(i) is not None:
                continue
            result = False
            for end_index, end in end_status_dict.items():
                for step_matrix in steps:
                    if step_matrix[i][end_index] == 1:
                        result = True
                        break
                if result is True:
                    break
            if result is False:
                self.add_warning(graph_name, 'end', status_dict.get(i))

        return result

    def _find_all_paths(self, matrix):
        bool_matrix = self._create_adjacency_matrix(matrix)
        steps = [bool_matrix]

        for i in range(len(matrix) - 1):
            steps.append(MultiplicationMatrix.direct_multiply(steps[0], steps[-1]))

        return steps

    def _check_graph(self, graph_statuses, graph_matrix, graph_name):
        start_statuses = self._determinate_marked_statuses(graph_statuses, 'start')
        end_statuses = self._determinate_marked_statuses(graph_statuses, 'end')

        index_statuses = self._determinate_marked_statuses(graph_statuses, None)
        index_statuses.update(start_statuses)
        index_statuses.update(end_statuses)

        steps = self._find_all_paths(graph_matrix)

        result = self._verify_start_graph(graph_name, start_statuses, index_statuses, steps)
        result = self._verify_end_graph(graph_name, end_statuses, index_statuses, steps) and result

        return result

    def _check_graph_mark(self, graph_statuses, graph_matrix, graph_name):
        #start_statuses = self._determinate_marked_statuses(graph_statuses, 'start')
        #end_statuses = self._determinate_marked_statuses(graph_statuses, 'end')

        #index_statuses = self._determinate_marked_statuses(graph_statuses, None)
        #index_statuses.update(start_statuses)
        #index_statuses.update(end_statuses)

        steps = self._find_all_paths(graph_matrix)

        #result = self._verify_start_graph(graph_name, start_statuses, index_statuses, steps)
        #result = self._verify_end_graph(graph_name, end_statuses, index_statuses, steps) and result

        return True

    def check_model(self, information_model):
        self.warnings.clear()
        self.errors.clear()
        #self.successes.clear()

        result = True
        statuses = dict()

        if isinstance(information_model, Model):
            for graph in information_model.schemes:
                result = self._check_graph(graph.statuses, graph.matrix, graph.name) and result
                for status, mark in graph.statuses.items():
                    if mark == 'start':
                        mark = None
                    statuses.update({graph.name+status: mark})

            result = self._check_graph(statuses, information_model.graph_matrix, information_model.name)

        return result

    def check_model_mark(self, information_model):



        return True


class GraphAdjacencyLists(BaseVerifier):
    def _verify_start_graph(self):
        pass

    def _verify_end_graph(self):
        pass

    def _bfs(self, graph, starts):
        nodes = [node for node in starts]
        visited = list(nodes)
        queue = [nodes]

        lasts = []

        while queue:
            temps = queue.pop()
            nodes = []

            for t in temps:
                if graph.get(t) is None:
                    lasts.append(t)
                else:
                    for neighbour in graph.get(t):
                        if neighbour not in visited and neighbour not in nodes:
                            nodes.append(neighbour)

            if len(nodes) > 0:
                queue.append(nodes)
                visited += nodes

        return visited, lasts

    def _dfs(self, graph, start, path=None, visited=None):
        if visited is None:
            visited = set()
            path = list()
        visited.add(start)
        path.append(start)

        if graph.get(start) is None:
            return start
        for next in set(graph.get(start)) - set(path):
            options = graph[start][next]
            flag = len(options) == 0
            for opt in options:
                if isinstance(opt.command, AllCommand):
                    for p in opt.parameters:
                        if path.count(p) > 0:
                            flag = True
                if isinstance(opt.command, AnyCommand):
                    for p in opt.parameters:
                        if path.count(p) > 0:
                            flag = True

            if flag:
                self._dfs(graph, next, path, visited)
        return visited, path[-1]

    def _check_graph(self, statuses, adjacency_list):
        start_statuses = list(self._determinate_marked_statuses(statuses, 'start').values())
        end_statuses = list(self._determinate_marked_statuses(statuses, 'end').values())
        all_statuses = set(statuses.keys())

        visited, lasts = self._bfs(adjacency_list, start_statuses)

        result = set(visited) == set(statuses.keys())

        err_starts = set(statuses.keys()) - set(visited)
        err_ends = set(lasts) - set(end_statuses)

        return result, err_starts, err_ends

    def _check_graph_mark(self, statuses, adjacency_list):
        start_statuses = list(self._determinate_marked_statuses(statuses, 'start').values())
        end_statuses = list(self._determinate_marked_statuses(statuses, 'end').values())
        all_statuses = set(statuses.keys())

        visitedes = []
        ends = []
        for start in start_statuses:
            visited, end = self._dfs(adjacency_list, start)
            visitedes.append(visited)
            ends.append(end)

        return True, ends

    def check_model(self, information_model):
        self.warnings.clear()
        self.errors.clear()
        #self.successes.clear()

        result = True
        statuses = dict()
        lists = dict()

        if isinstance(information_model, Model):
            for graph in information_model.schemes:
                res, starts, ends = self._check_graph(graph.statuses, graph.adjacency_list)
                result = res and result
                for warn in starts:
                    self.add_warning(graph.name, 'start', warn)
                for warn in ends:
                    self.add_warning(graph.name, 'end', warn)
                for status, value in graph.adjacency_list.items():
                    t = dict()
                    for next_status, options in value.items():
                        t.update({graph.name + next_status: options})
                    lists.update({graph.name + status: t})
                for status, mark in graph.statuses.items():
                    statuses.update({graph.name + status: mark})

            for trans in information_model.graph_transition_list:
                lists.update({trans.graph + trans.status: {trans.graph + trans.status: trans.options}})

            result, starts, ends = self._check_graph(statuses, lists)

            for err in starts:
                self.add_error(information_model.name, 'start', err)
            for err in ends:
                self.add_error(information_model.name, 'end', err)

        return result

    def check_model_mark(self, information_model):
        self.warnings.clear()
        self.errors.clear()
        #self.successes.clear()

        result = True
        statuses = dict()
        lists = dict()

        if isinstance(information_model, Model):
            for graph in information_model.schemes:
                res, end = self._check_graph_mark(graph.statuses, graph.adjacency_list)
                result = res and result
                #print(smt)
                """for warn in starts:
                    self.add_warning(graph.name, 'start', warn)
                for warn in ends:
                    self.add_warning(graph.name, 'end', warn)
                for status, value in graph.adjacency_list.items():
                    t = dict()
                    for next_status, options in value.items():
                        t.update({graph.name + next_status: options})
                    lists.update({graph.name + status: t})
                for status, mark in graph.statuses.items():
                    statuses.update({graph.name + status: mark})

            for trans in information_model.graph_transition_list:
                lists.update({trans.graph + trans.status: {trans.graph + trans.status: trans.options}})

            result, starts, ends = self._check_graph(statuses, lists)

            for err in starts:
                self.add_error(information_model.name, 'start', err)
            for err in ends:
                self.add_error(information_model.name, 'end', err)
            """
        return self.check_model(information_model)


class Checker:
    def __init__(self, verifier):
        self.checker = verifier#GraphAdjacencyLists()#GraphMatrixVerifier()

    def check(self, model):
        # return self.checker.check_model_mark(model)
       return self.checker.check_model(model)

    def get_errors(self):
        return self.checker.errors

    def get_warnings(self):
        return self.checker.warnings
