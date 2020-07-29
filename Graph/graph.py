import graphviz
import os
import math
import random
import copy

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'


class Node:
    def __init__(self, name):
        self.name = name
        self.neighbours = []  # all nodes adjacent to this one
        self.distances = {}  # the length of all threads from this node to each adjacent node

    def add_connection(self, neigh, distance, two_way=False):
        """generates a thread between the current node and another one that is given(neigh)"""
        if neigh not in self.neighbours and neigh is not self:  # checks if a thread can exist or already exists
            self.neighbours.append(neigh)
            self.distances[neigh.name] = distance
            if two_way:  # if true generates a reverse thread
                neigh.add_connection(self, distance)
                neigh.distances[self.name] = distance

    def remove_connection(self, neigh, two_way=False):
        """deletes a thread between the current node and another one that is given(neigh)"""
        if neigh in self.neighbours and neigh is not self:
            self.neighbours.remove(neigh)
            del self.distances[neigh.name]
            if two_way:  # if true deletes the reverse thread too
                neigh.remove_connection(self)
                del neigh.distances[self.name]


class GraphNetwork:
    def __init__(self):
        self.nodes = []
        self.generate_nodes()
        self.generate_random_threads()
        self.print_graph()
        for node in self.nodes:  # applies the dijkstra algorithm to each node
            self.dijkstra_algorthm(node)

    def generate_random_threads(self):
        for node in self.nodes:
            number_of_threads = random.randint(1, int(len(self.nodes) / 3))
            for _ in range(number_of_threads):
                values = self.generate_random_idx_distance(len(self.nodes), 10)
                node.add_connection(self.nodes[values[0]], values[1])

    def generate_random_idx_distance(self, idx_max, distance_max):
        idx = random.randint(0, idx_max - 1)
        distance = random.randint(1, distance_max)
        return idx, distance

    def generate_nodes(self):
        inp = input("How many nodes to generate?: ")
        if inp.isdigit():  # check if input is a number
            for num in range(int(inp)):  # Node factory
                a = Node("Node_" + str(num))
                self.nodes.append(a)
        else:
            print("Invalid input!!! Please type an integer!!!")
            self.generate_nodes()

    def print_graph(self):
        """Print a scheme of the graph using graphviz"""
        g = graphviz.Digraph("graph.png", format="png")
        for node in self.nodes:
            for neigh in node.neighbours:
                g.edge(node.name, neigh.name, label=str(node.distances[neigh.name]))
        g.render()

    def dijkstra_algorthm(self, starting_node):
        """Applies the dijkstra algorithm for a specific node by finding the shortest path to each other node"""
        dijkstra_dict = {}
        dijkstra_nodes = copy.copy(self.nodes)
        """generates initial values in dijkstra algorithm - one 0 and the rest are equal to infinity"""
        for node in dijkstra_nodes:
            dijkstra_dict[node.name] = math.inf
            if node == starting_node:
                dijkstra_dict[node.name] = 0
        """First iteration - applies all the distances from the starting node to all of its adjacent nodes"""
        for neigh in starting_node.neighbours:
            dijkstra_dict[neigh.name] = starting_node.distances[neigh.name]
        dijkstra_nodes.remove(starting_node)  # we dont need this node for further iterations
        while dijkstra_nodes != []:  # each iterations removes one node so when list is empty the algorithm is complete
            chosen_node = self.smallest_dict_value(dijkstra_dict, dijkstra_nodes)
            if self.dijkstra_step(dijkstra_dict, chosen_node=chosen_node) == None:
                break  # exit the loop if no more nodes are reachable from the starting node
            dijkstra_nodes.remove(chosen_node)  # we dont need this node for further iterations
        self.print_dijkstra(dijkstra_dict, starting_node)

    def print_dijkstra(self, dict, starting_node):
        print(starting_node.name)
        for key in dict.keys():
            if dict[key] != math.inf:  # print all non infinite values
                print(key + " : " + str(dict[key]), end="  |  ")
        print("\n")

    def smallest_dict_value(self, dict, list_of_keys):
        """Returns the next node needed forthe next iteration"""
        smallest_distance = math.inf
        searched_node = None  # if all values left are equal to infinity, returns None and stops the algorithm
        for node in list_of_keys:
            if dict[node.name] < smallest_distance:
                smallest_distance = dict[node.name]
                searched_node = node
        return searched_node

    def dijkstra_step(self, dict, chosen_node=None):
        """Applies a single iteration of the dijkstra algorithm"""
        if chosen_node == None:
            return None
        else:
            for neigh in chosen_node.neighbours:  # goes through all adjacent nodes and looks for a shorter path
                if dict[neigh.name] > dict[chosen_node.name] + chosen_node.distances[neigh.name]:
                    dict[neigh.name] = dict[chosen_node.name] + chosen_node.distances[neigh.name]
            return True



a = GraphNetwork()
