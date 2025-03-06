# Created on 02/05/2025
# Author: Frank Vega

import itertools
import networkx as nx

def find_dominating_set(graph: nx.Graph):
    """
    Computes an approximate Dominating Set for an undirected graph in polynomial time.
    
    Args:
        graph (nx.Graph): A NetworkX Graph object representing the input graph.
                          Must be undirected.
    
    Returns:
        set: A set of vertex indices representing the approximate Dominating Set.
             Returns an empty set if the graph is empty or has no edges.
    """
    # Validate input graph
    if not isinstance(graph, nx.Graph):
        raise ValueError("Input must be an undirected NetworkX Graph.")
    if graph.is_directed():
        raise ValueError("Input graph must be undirected.")
    
    # Handle empty graph or graph with no edges
    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return set()
    
    # Remove isolated nodes (nodes with no edges) as they are not part of any Dominating Set
    isolated_nodes = list(nx.isolates(graph))
    graph.remove_nodes_from(isolated_nodes)
    
    # If the graph becomes empty after removing isolated nodes, return an empty set
    if graph.number_of_nodes() == 0:
        return set()
    
    # Compute approximate minimum maximal matching (2-approximation)
    edges = nx.approximation.min_maximal_matching(graph)

    # Create a set of nodes from the edges
    dominating_set = {node for edge in edges for node in edge}

    # Remove redundant vertices from the candidate Dominating Set
    changed = True
    while changed:
        changed = False
        for vertex in list(dominating_set):
            if nx.is_dominating_set(graph, dominating_set - {vertex}):
                dominating_set.remove(vertex)
                changed = True
    
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