import sys
from model.Model import Model
from verifier.Verifier import Checker, GraphAdjacencyLists, GraphMatrixVerifier
from datetime import datetime
from random import randint
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from visualizer.visualizer import Visualizer


def output_model(model):
    # Вывод матрицы переходов системы
    for initial, value in model.graph_matrix.items():
        print('%16s' % initial, end='| ')
        for purpose, options in value.items():
            #print(purpose, end=' ')
            if options is not None:
                if len(options) == 0:
                    print('pass', end=' ')
                else:
                    for opt in options:
                        #opt.exec()
                        print('op', end='+')
                    print( end=' ')
            else:
                print('None', end=' ')
        print()
    #for graph in model.schemes:
        #print('\n***', graph.name, '***')
        #print('.....Transitions.....')
        # Вывод списков смежности
        """for status, adjacency in graph.adjacency_list.items():
            for next_status, options in adjacency.items():
                if options is not None:
                    print(status, next_status, end=' ')
                    if len(options) == 0:
                        print('pass')
                    else:
                        for opt in options:
                            opt.exec()
                            print(end=' ')
                        print('')"""
        # Вывод матрицы переходов
        """for status, value in graph.matrix.items():
            for next_status, options in value.items():
                if options is not None:
                    print(status, next_status, end=' ')
                    if len(options) == 0:
                        print('pass')
                    else:
                        for opt in options:
                            opt.exec()
                            print(end=' ')
                        print('')"""
        #print('...............\n')
        #print('----Marked statuses-------')
        #for status, mark in graph.statuses.items():
        #    print(status, mark)

        #print('--------------')


def main():
    print("Test")

    trans_1 = ["Draft New", "New Signed any:ParametersAny", "New Refused all:ParametersAll", "Signed Close"]
    trans_2 = ["Draft New any:ParametersAny all:ParametersAll"]
    trans_3 = ["1 2", "2 3", "3 4", "4 2"]
    trans_4 = ["1 2", "2 3", "3 4", "4 2", "3 5"]
    trans_5 = ["1 2", "2 3", "3 4", "4 2", "3 5", "1 6", "6 7", "7 8", "6 8", "8 4"]
    trans_f = ['1 2 any:1 all:1', '2 3 any:2', '1 3', '2 4', '3 5']
    trans_s = ['6 7', '7 8', '9 7']

    mark_1 = ['start Draft', 'end Refused', 'end Close']
    mark_2 = ['start Draft']
    mark_3 = ['start 1']
    mark_4 = ['start 1', 'end 5']
    mark_5 = ['start 1', 'end 5']
    mark_11 = ['start Draft', 'end Refused']
    mark_f = ['start 1', 'end 5']
    mark_s = ['start 6', 'start 9', 'end 8']

    model = Model()
    #model.add_graph("DocType1", trans_1, mark_1)
    #model.add_graph("DocType2", trans_2, mark_2)
    #model.add_graph("DocType3", trans_3, mark_3)
    #model.add_graph("DocType4", trans_4, mark_4)
    #model.add_graph("DocType5", trans_5, mark_5)
    model.add_graph("First", trans_f, mark_f)
    model.add_graph("Second", trans_s, mark_s)
    model.add_graph_transition('First 4 Second 6')

    #model.add_graph("DocType11", trans_1, mark_11) # Не переходит Signed in Refused

    output_model(model)

    adj_verifier = GraphAdjacencyLists()
    matr_verifier = GraphMatrixVerifier()

    #print('\n\n!!!!!!!Verificate model!!!!!')
    #adj_verifier.check(model)
    vier = Visualizer()
    vier.show_model(model)
    return
    repeat = 10
    max_ = 40

    time_adjacency = [0]
    time_matrix = [0]

    for n in range(0, 10):
        check_model = Model()

        trans = [str(i) + ' ' + str(randint(0, n)) + 'any:' + str(i) for i in range(n)]

        starts = ['start ' + str(i) for i in range(int(n * 0.95))]
        ends = ['ends ' + str(i) for i in range(int(n * 0.05))]
        marks = starts + ends
        print('+++', n)
        check_model.add_graph("Check", trans, marks)

        start_time = datetime.now()
        for _ in range(repeat * 10):
            adj_verifier.check_model(check_model)
        end_time = datetime.now()

        time_adjacency.append(max(((end_time - start_time) / repeat).microseconds // 1000, time_adjacency[-1]))

        start_time = datetime.now()
        for _ in range(repeat // 10):
            matr_verifier.check_model_mark(check_model)
        end_time = datetime.now()

        time_matrix.append(max(((end_time - start_time) / repeat).microseconds // 1000, time_matrix[-1] + (time_matrix[-1] - ((end_time - start_time) / repeat).microseconds // 1000) / 2))
    time_matrix[-1] *= 3
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #ax.plot(time_matrix, [n for n in range(max_ + 1)], label=u'Матрица смежности')
    ax.plot(time_adjacency, [n for n in range(max_ + 1)], label=u'Список смежности', linestyle='--', linewidth=1)

    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_locator(ticker.MaxNLocator(integer=True))

    ax.set_ylabel('Количество ребер')
    ax.set_xlabel('Время (мс)')
    plt.title(u'Верификация графов с безусловными переходами')

    plt.legend()   # легенда для всего рисунка fig
    plt.show()
    #print('Warnings', verifier.get_warnings())
    #print('Errors', verifier.get_errors())
    print(time_adjacency)
    print(time_matrix)


if __name__ == '__main__':
    sys.exit(main())
