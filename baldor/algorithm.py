# Created on 02/05/2025
# Author: Frank Vega

import itertools
import networkx as nx
import numpy as np
from . import utils

def find_vertex_cover(graph):
    """
    Computes an approximate vertex cover in polynomial time.

    Args:
        graph: A NetworkX graph.

    Returns:
        A set of vertex indices representing the approximate vertex cover, or None if the graph is empty.
    """

    # Handle empty graph
    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return None

    if graph.number_of_nodes()**2 >= graph.number_of_edges()**3:
        approximate_vertex_cover = find_vertex_cover_in_sparse_graph(graph)
    else:
        approximate_vertex_cover = find_vertex_cover_in_dense_graph(graph)    

    return approximate_vertex_cover


def find_vertex_cover_in_dense_graph(graph):
    """
    Computes an approximate vertex cover in polynomial time.

    Args:
        graph: A NetworkX graph.

    Returns:
        A set of vertex indices representing the approximate vertex cover, or None if the graph is empty.
    """

    # Handle empty graph
    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return None

    approximate_vertex_cover = set()
    components = list(nx.connected_components(graph))

    while components:
        component = components.pop()
        subgraph = graph.subgraph(component)

        if subgraph.number_of_edges() > 0:
            if nx.is_bipartite(subgraph):
                # Use Hopcroft-Karp algorithm for bipartite graphs
                bipartite_matching = nx.bipartite.hopcroft_karp_matching(subgraph)
                bipartite_vertex_cover = nx.bipartite.to_vertex_cover(subgraph, bipartite_matching)
                approximate_vertex_cover.update(bipartite_vertex_cover)
            elif subgraph.number_of_nodes()**2 >= subgraph.number_of_edges()**3:
                approximate_vertex_cover.update(find_vertex_cover_in_sparse_graph(subgraph))            
            else:
                # Use maximal matching for non-bipartite graphs
                maximal_matching = nx.maximal_matching(subgraph)
                candidate1 = {min(u, v) for u, v in maximal_matching}
                candidate2 = {max(u, v) for u, v in maximal_matching}

                # Choose the candidate with the higher total degree
                if sum((subgraph.degree(u) - 1) for u in candidate1) >= sum((subgraph.degree(v) - 1) for v in candidate2):
                    best_candidate = candidate1
                else:
                    best_candidate = candidate2

                approximate_vertex_cover.update(best_candidate)

                # Remove the selected nodes and add the remaining components
                residual_graph = subgraph.copy()
                residual_graph.remove_nodes_from(best_candidate)
                components.extend(nx.connected_components(residual_graph))

    return approximate_vertex_cover


def find_vertex_cover_in_sparse_graph(graph):
    """
    Computes an approximate vertex cover in polynomial time.

    Args:
        graph: A NetworkX graph.

    Returns:
        A set of vertex indices representing the approximate vertex cover, or None if the graph is empty.
    """

    # Handle empty graph
    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return None

    # The maximum node in the input graph plus 1.    
    n = max(graph.nodes()) + 1
  
    # Create an edge graph where each node represents an edge in the original graph
    edge_graph = nx.Graph()
    for u, v in graph.edges():
        # Minimum and maximum vertices
        minimum = min(u, v)
        maximum = max(u, v)
        # Unique representation of the edge
        edge = n * minimum + maximum
        # Avoid the case when u = v
        if minimum != maximum:
            for a in graph.neighbors(minimum):
                if maximum < a:
                    adjacent_edge = n * minimum + a
                    edge_graph.add_edge(edge, adjacent_edge)
            for b in graph.neighbors(maximum):
                if b < minimum:
                    adjacent_edge = n * b + maximum
                    edge_graph.add_edge(edge, adjacent_edge)

    # Find the minimum edge cover in the edge graph
    min_edge_cover = nx.min_edge_cover(edge_graph)

    # Convert the edge cover back to a vertex cover
    vertex_cover = set()
    for edge1, edge2 in min_edge_cover:
        # Extract the common vertex between the two edges
        common_vertex = (edge1 // n) if (edge1 // n) == (edge2 // n) else (edge1 % n)
        vertex_cover.add(common_vertex)

    # Include isolated edges (edges not covered by the vertex cover)
    for u, v in graph.edges():
        if u not in vertex_cover and v not in vertex_cover:
            vertex_cover.add(u)

    # Remove redundant vertices from the vertex cover
    approximate_vertex_cover = set(vertex_cover)
    for u in vertex_cover:
        # Check if removing the vertex still results in a valid vertex cover
        if utils.is_vertex_cover(graph, approximate_vertex_cover - {u}):
            approximate_vertex_cover.remove(u)

    return approximate_vertex_cover

 
def find_vertex_cover_brute_force(graph):
    """
    Calculates the exact minimum vertex cover using brute-force (exponential time).

    Args:
        graph: A NetworkX graph.

    Returns:
        A set of vertex indices representing the minimum vertex cover, or None if the graph is empty.
    """
    
    # Handle empty graph
    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return None

    # The maximum node in the input graph.    
    n_vertices = max(graph.nodes()) + 1
 

    for k in range(1, n_vertices + 1): # Iterate through all possible sizes of the cover
        for cover_candidate in itertools.combinations(range(n_vertices), k):
            cover_candidate = set(cover_candidate)
            if utils.is_vertex_cover(graph, cover_candidate):
                return cover_candidate
                
    return None



def find_vertex_cover_approximation(graph):
    """
    Calculates the approximate vertex cover using an approximation of at most 2.

    Args:
        graph: A NetworkX graph.

    Returns:
        A set of vertex indices representing the approximate vertex cover, or None if the graph is empty.
    """

    # Handle empty graph
    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return None

    #networkx doesn't have a guaranteed minimum vertex cover function, so we use approximation
    vertex_cover = nx.approximation.vertex_cover.min_weighted_vertex_cover(graph)
    return vertex_cover