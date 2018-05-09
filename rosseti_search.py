import networkx as nx
import random
from operator import itemgetter
from typing import List, Set, NamedTuple, Callable

N_RESULTS = 8
THRESHOLD = 0.2
K = 6

# special type containing the node id and its calculated heuristic
class NodeInfo(NamedTuple):
    id: int
    heuristic_val: float

# returns the calculated heuristic of a given node
def calc_heuristic(graph: nx.Graph, node: int) -> float:
    node_degree = graph.degree(node)
    heuristic_value = node_degree
    for neighbor in graph.neighbors(node):
        heuristic_value += graph.degree(neighbor) * 0.8
    return heuristic_value

# cutoff function so you dont have to look up all the edges on search (using the biggest neighbors heuristic-based)
def get_k_neighbors_with_biggest_heuristic(graph: nx.Graph,
                                           nodes: Set[int],
                                           k: int,
                                           visited: Set[int]) -> List[NodeInfo]:
    ids_and_heuristic: List[NodeInfo] = [NodeInfo(i, calc_heuristic(graph, i)) for i in nodes - visited]
    ids_and_heuristic.sort(key=itemgetter(1), reverse=True)
    return ids_and_heuristic[:k]

# cutoff function so you dont have to look up all the edges on search (using a random criteria)
def get_sample_of_neighbors(graph: nx.Graph,
                            nodes: Set[int],
                            k: int,
                            visited: Set[int]) -> List[NodeInfo]:
    ids_and_heuristic: List[NodeInfo] = [NodeInfo(i, calc_heuristic(graph, i)) for i in nodes - visited]
    return random.sample(ids_and_heuristic, min(k, len(ids_and_heuristic)))

# updates the frontier structure with biggest found yet
def update_most_influential(cur_list: List[NodeInfo], new_elems: List[NodeInfo]):
    for elem in new_elems:
        if elem.heuristic_val > cur_list[-1].heuristic_val:
            cur_list[-1] = elem
            cur_list.sort(key=itemgetter(1), reverse=True)

# search function \o/
def search(graph: nx.Graph,
           origin_node: int,
           k_most_influential: List[NodeInfo],  # That times cover was just confirmation
           k: int,
           neighbors_selection_function: Callable):

    visited: Set[int] = {origin_node}  # to check the visited nodes
    # creates a list of the next nodes to look up based on the cutoff function chosen
    next_nodes: List[NodeInfo] = [NodeInfo(origin_node, calc_heuristic(graph, origin_node))]

    while True:  # dfs loop starts
        all_neighbor_ids: Set[int] = set()  # holds all the neighbors ids checked until now

        for neighbor in next_nodes:  # limited bfs looking only one layer around
            all_neighbor_ids = all_neighbor_ids.union(graph.neighbors(neighbor.id)) #update neighbors

        next_nodes = neighbors_selection_function(graph, all_neighbor_ids, k, visited)  # update neighbors based on cutoff function

        update_most_influential(k_most_influential, next_nodes)  # update the structure containing the result

        if not len(next_nodes):
            break
        if next_nodes[0].heuristic_val < k_most_influential[0].heuristic_val * THRESHOLD:  # limits dfs by heuristic
            break

        visited = visited.union(all_neighbor_ids)  # visit neighbors so we dont need to look again


def count_visits(graph: nx.Graph, node: int) -> int:
    visited: Set[int] = {node}
    next_neighbors: Set[int] = set(graph.neighbors(node))

    while len(next_neighbors) > 0:
        visited = visited.union(next_neighbors)
        the_next: Set = set()
        for node in next_neighbors:
            the_next = the_next.union(graph.neighbors(node))
        next_neighbors = the_next - visited

    return len(visited)


if __name__ == '__main__':
    print("K =", K)
    G = nx.Graph()
    with open('facebook_combined.txt', 'r') as file:
        for line in file:
            G.add_edge(*map(int, line.split()))

    node_with_most_neighbors = max(dict(G.degree).items(), key=itemgetter(1))

    k_most_influential: List[NodeInfo] = [NodeInfo(node_with_most_neighbors[0],
                                                   calc_heuristic(G, node_with_most_neighbors[0]))]

    for _ in range(N_RESULTS - 1):
        k_most_influential.append(NodeInfo(0, -999))

    search(G, node_with_most_neighbors[0], k_most_influential, K, get_k_neighbors_with_biggest_heuristic)

    print("Search using K biggest")
    print(k_most_influential)

    for info in k_most_influential:
        print(info.id, count_visits(G, info.id))

    k_most_influential: List[NodeInfo] = [NodeInfo(node_with_most_neighbors[0],
                                                   calc_heuristic(G, node_with_most_neighbors[0]))]

    for _ in range(N_RESULTS - 1):
        k_most_influential.append(NodeInfo(0, -999))

    search(G, node_with_most_neighbors[0], k_most_influential, K, get_sample_of_neighbors)
    print("Search using K random")
    print(k_most_influential)
    for info in k_most_influential:
        print(info.id, count_visits(G, info.id))