# Created on 02/05/2025
# Author: Frank Vega

import itertools
from . import utils

import networkx as nx

def find_dominating_set(graph):
    """
    Approximate minimum dominating set for an undirected graph by transforming it into a bipartite graph.

    Args:
        graph (nx.Graph): A NetworkX Graph object representing the input graph.

    Returns:
        set: A set of vertex indices representing the approximate minimum dominating set.
             Returns an empty set if the graph is empty or has no edges.
    """
    # Subroutine to compute a dominating set in a bipartite component, used to find a dominating set in the original graph
    def find_dominating_set_via_bipartite_proxy(G):
        # Initialize an empty set to store the dominating set for this bipartite component
        dominating_set = set()
        # Track which vertices in the bipartite graph are dominated
        dominated = {v: False for v in G.nodes()}
        # Sort vertices by degree (ascending) to prioritize low-degree nodes for greedy selection
        undominated = sorted(list(G.nodes()), key=lambda x: len(list(G.neighbors(x))))
        
        # Continue processing until all vertices are dominated
        while undominated:
            # Pop the next vertex to process (starting with lowest degree)
            v = undominated.pop()
            # Check if the vertex is not yet dominated
            if not dominated[v]:
                # Initialize the best vertex to add as the current vertex
                best_vertex = v
                # Initialize the count of undominated vertices covered by the best vertex
                best_undominated_count = -1

                # Consider the current vertex and its neighbors as candidates
                for neighbor in list(G.neighbors(v)) + [v]:
                    # Count how many undominated vertices this candidate covers
                    undominated_neighbors_count = 0
                    for u in list(G.neighbors(neighbor)) + [neighbor]:
                        if not dominated[u]:
                            undominated_neighbors_count += 1

                    # Update the best vertex if this candidate covers more undominated vertices
                    if undominated_neighbors_count > best_undominated_count:
                        best_undominated_count = undominated_neighbors_count
                        best_vertex = neighbor

                # Add the best vertex to the dominating set for this component
                dominating_set.add(best_vertex)

                # Mark the neighbors of the best vertex as dominated
                for neighbor in G.neighbors(best_vertex):
                    dominated[neighbor] = True
                    # Mark the mirror vertex (i, 1-k) as dominated to reflect domination in the original graph
                    mirror_neighbor = (neighbor[0], 1 - neighbor[1])
                    dominated[mirror_neighbor] = True

        # Return the dominating set for this bipartite component
        return dominating_set

    # Validate that the input is a NetworkX Graph object
    if not isinstance(graph, nx.Graph):
        raise ValueError("Input must be an undirected NetworkX Graph.")

    # Handle edge cases: return an empty set if the graph has no nodes or no edges
    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return set()

    # Initialize the dominating set with all isolated nodes, as they must be included to dominate themselves
    approximate_dominating_set = set(nx.isolates(graph))
    # Remove isolated nodes from the graph to process the remaining components
    graph.remove_nodes_from(approximate_dominating_set)

    # If the graph is empty after removing isolated nodes, return the set of isolated nodes
    if graph.number_of_nodes() == 0:
        return approximate_dominating_set

    # Initialize an empty bipartite graph to transform the remaining graph
    bipartite_graph = nx.Graph()
        
    # Construct the bipartite graph B
    for i in graph.nodes():
        # Add an edge between mirror nodes (i, 0) and (i, 1) for each vertex i
        bipartite_graph.add_edge((i, 0), (i, 1))
        # Add edges reflecting adjacency in the original graph: (i, 0) to (j, 1) for each neighbor j
        for j in graph.neighbors(i):
            bipartite_graph.add_edge((i, 0), (j, 1))
    
    # Process each connected component in the bipartite graph
    for component in nx.connected_components(bipartite_graph):
        # Extract the subgraph for the current connected component
        bipartite_subgraph = bipartite_graph.subgraph(component)

        # Compute the dominating set for this component using the subroutine
        tuple_nodes = find_dominating_set_via_bipartite_proxy(bipartite_subgraph)

        # Extract the original node indices from the tuple nodes (i, k) and add them to the dominating set
        approximate_dominating_set.update({tuple_node[0] for tuple_node in tuple_nodes})

    # Return the final dominating set for the original graph
    return approximate_dominating_set

def find_dominating_set_brute_force(graph):
    """
    Computes an exact minimum dominating set in exponential time.

    Args:
        graph: A NetworkX Graph.

    Returns:
        A set of vertex indices representing the exact dominating set, or None if the graph is empty.
    """

    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return None

    n_vertices = len(graph.nodes())

    for k in range(1, n_vertices + 1): # Iterate through all possible sizes of the cover
        for candidate in itertools.combinations(graph.nodes(), k):
            cover_candidate = set(candidate)
            if nx.dominating.is_dominating_set(graph, cover_candidate):
                return cover_candidate
                
    return None



def find_dominating_set_approximation(graph):
    """
    Computes an approximate dominating set in polynomial time with a logarithmic approximation ratio for undirected graphs.

    Args:
        graph: A NetworkX Graph.

    Returns:
        A set of vertex indices representing the approximate dominating set, or None if the graph is empty.
    """

    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return None

    #networkx doesn't have a guaranteed minimum dominating set function, so we use approximation
    dominating_set = nx.approximation.dominating_set.min_weighted_dominating_set(graph)
    return dominating_set