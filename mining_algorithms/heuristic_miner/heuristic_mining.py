import numpy as np
from mining_algorithms.ddcal_clustering import DensityDistributionClusterAlgorithm
from graphs.visualization.heuristic_graph import HeuristicGraph


class HeuristicMining:
    def __init__(self, log):
        self.log = log
        self.events, self.appearence_frequency = self.__filter_out_all_events()
        self.succession_matrix = self.__create_succession_matrix()
        self.dependency_matrix = self.__create_dependency_matrix()

        # Graph modifiers
        self.min_edge_thickness = 1
        # self.max_node_size = 10
        self.min_node_size = 1.5
        self.min_frequency = 1
        self.dependency_threshold = 0.5

    def create_dependency_graph_with_graphviz(
        self, dependency_threshold, min_frequency
    ):
        dependency_graph = self.__create_dependency_graph(
            dependency_threshold, min_frequency
        )
        self.dependency_threshold = dependency_threshold
        self.min_frequency = min_frequency

        # create graph
        graph = HeuristicGraph()
        # cluster the node sizes based on frequency
        cluster = DensityDistributionClusterAlgorithm(
            list(self.appearence_frequency.values())
        )
        freq_sorted = list(cluster.sorted_data)
        freq_labels_sorted = list(cluster.labels_sorted_data)

        # add nodes to graph
        for node in self.events:
            node_freq = self.appearence_frequency.get(node)
            w = (
                freq_labels_sorted[freq_sorted.index(node_freq)] / 2
                + self.min_node_size
            )
            h = w / 3
            graph.add_event(node, node_freq, (w, h))

        # cluster the edge thickness sizes based on frequency
        edge_frequencies = self.dependency_matrix.flatten()
        edge_frequencies = edge_frequencies[edge_frequencies >= 0.0]
        edge_frequencies = np.unique(edge_frequencies)
        # print(edge_frequencies)
        cluster = DensityDistributionClusterAlgorithm(edge_frequencies)
        freq_sorted = list(cluster.sorted_data)
        freq_labels_sorted = list(cluster.labels_sorted_data)

        # add edges to graph
        for i in range(len(self.events)):
            for j in range(len(self.events)):
                if dependency_graph[i][j] == 1.0:
                    if dependency_threshold == 0:
                        edge_thickness = 0.1
                    else:
                        edge_thickness = (
                            freq_labels_sorted[
                                freq_sorted.index(self.dependency_matrix[i][j])
                            ]
                            + self.min_edge_thickness
                        )
                    graph.create_edge(
                        self.events[i],
                        self.events[j],
                        weight=int(self.succession_matrix[i][j]),
                        size=edge_thickness,
                    )
        graph.add_start_node()

        graph.add_starting_edges(self.__get_start_nodes())

        graph.add_end_node()
        graph.add_ending_edges(self.__get_end_nodes())

        return graph

    def get_max_frequency(self):
        max_freq = 0
        for value in list(self.appearence_frequency.values()):
            if value > max_freq:
                max_freq = value
        return max_freq

    def get_min_frequency(self):
        return self.min_frequency

    def get_threshold(self):
        return self.dependency_threshold

    def __filter_out_all_events(self):
        dic = {}
        for trace in self.log:
            for activity in trace:
                if activity in dic:
                    dic[activity] = dic[activity] + 1
                else:
                    dic[activity] = 1

        activities = list(dic.keys())
        return activities, dic

    def __create_succession_matrix(self):
        succession_matrix = np.zeros((len(self.events), len(self.events)))
        for trace in self.log:
            index_x = -1
            for element in trace:

                if index_x < 0:
                    index_x += 1
                    continue
                x = self.events.index(trace[index_x])
                y = self.events.index(element)
                succession_matrix[x][y] += 1
                index_x += 1
        return succession_matrix

    def __get_start_nodes(self):
        # a start node is a node where an entire column in the succession_matrix is 0.
        start_nodes = []
        for case in self.log:
            if case[0] not in start_nodes:
                start_nodes.append(case[0])

        return start_nodes

    def __get_end_nodes(self):
        # an end node is a node where an entire row in the succession_matrix is 0.
        end_nodes = []
        for case in self.log:
            last_index = len(case) - 1
            if case[last_index] not in end_nodes:
                end_nodes.append(case[last_index])

        return end_nodes

    def __create_dependency_matrix(self):
        dependency_matrix = np.zeros(self.succession_matrix.shape)
        y = 0
        for row in self.succession_matrix:
            x = 0
            for i in row:
                if x == y:
                    dependency_matrix[x][y] = self.succession_matrix[x][y] / (
                        self.succession_matrix[x][y] + 1
                    )
                else:
                    dependency_matrix[x][y] = (
                        self.succession_matrix[x][y] - self.succession_matrix[y][x]
                    ) / (
                        self.succession_matrix[x][y] + self.succession_matrix[y][x] + 1
                    )
                x += 1
            y += 1
        return dependency_matrix

    def __create_dependency_graph(self, dependency_treshhold, min_frequency):
        dependency_graph = np.zeros(self.dependency_matrix.shape)
        y = 0
        for row in dependency_graph:
            for x in range(len(row)):
                if (
                    self.dependency_matrix[y][x] >= dependency_treshhold
                    and self.succession_matrix[y][x] >= min_frequency
                ):
                    dependency_graph[y][x] += 1
            y += 1

        return dependency_graph