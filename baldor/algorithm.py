# Created on 02/05/2025
# Author: Frank Vega

import itertools
from . import utils
from . import dominating

import networkx as nx

def find_dominating_set(graph):
    """
    Computes an approximate Dominating Set for an undirected graph in polynomial time.
    The algorithm uses edge covers and dominating sets on trees to achieve
    a sublogarithmic approximation ratio.

    Args:
        graph (nx.Graph): A NetworkX Graph object representing the input graph.

    Returns:
        set: A set of vertex indices representing the approximate Dominating Set.
             Returns None if the graph is empty or has no edges.
    """

    # Handle empty graph or graph with no edges
    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return None

    # Remove isolated nodes (nodes with no edges) as they are not part of any Dominating Set
    graph.remove_nodes_from(list(nx.isolates(graph)))

    # Initialize an empty set to store the approximate Dominating Set
    approximate_dominating_set = set()

    # Find a minimum edge cover in the graph
    min_edge_cover = nx.min_edge_cover(graph)

    # Create a subgraph using the edges from the minimum edge cover
    min_edge_graph = nx.Graph(min_edge_cover)

    # Iterate over all connected components of the min_edge_graph
    for connected_component in nx.connected_components(min_edge_graph):
        # Create a subgraph for the current connected component
        subgraph = min_edge_graph.subgraph(connected_component)

        # Find a Dominating Set in the acyclic subgraph
        dominating_set = dominating.min_dominating_set_tree(subgraph)

        # Add the vertices from this connected component to the final Dominating Set
        approximate_dominating_set.update(dominating_set)
    
    # Remove redundant vertices from the candidate Dominating Set
    dominating_set = set(approximate_dominating_set)
    for u in approximate_dominating_set:
        # Check if removing the vertex still results in a valid Dominating Set
        if nx.dominating.is_dominating_set(graph, dominating_set - {u}):
            dominating_set.remove(u)

    return dominating_set

def find_dominating_set_brute_force(graph):
    """
    Computes an exact minimum Dominating Set in exponential time.

    Args:
        graph: A NetworkX Graph.

    Returns:
        A set of vertex indices representing the exact Dominating Set, or None if the graph is empty.
    """

    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return None

    n_vertices = len(graph.nodes())

    for k in range(1, n_vertices + 1): # Iterate through all possible sizes of the dominating sets
        for candidate in itertools.combinations(graph.nodes(), k):
            dominating_candidate = set(candidate)
            if nx.dominating.is_dominating_set(graph, dominating_candidate):
                return dominating_candidate
                
    return None



def find_dominating_set_approximation(graph):
    """
    Computes an approximate Dominating Set in polynomial time with a logarithmic approximation ratio for undirected graphs.

    Args:
        graph: A NetworkX Graph.

    Returns:
        A set of vertex indices representing the approximate Dominating Set, or None if the graph is empty.
    """

    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return None

    #networkx doesn't have a guaranteed minimum Dominating Set function, so we use approximation
    dominating_set = nx.approximation.dominating_set.min_weighted_dominating_set(graph)
    return dominating_set