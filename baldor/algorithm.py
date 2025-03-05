# Created on 02/05/2025
# Author: Frank Vega

import itertools
import networkx as nx

def min_dominating_set_tree(tree):
    """
    Find the minimum dominating set in a tree using dynamic programming.
    
    Parameters:
    tree (nx.Graph): A NetworkX graph that is a tree
    
    Returns:
    set: A minimum dominating set of the tree
    """
    # Check if the input is actually a tree
    if not nx.is_tree(tree):
        raise ValueError("Input graph is not a tree")
    
    # If the tree is empty, return an empty set
    if tree.number_of_nodes() == 0:
        return set()
    
    # If the tree has only one node, return that node
    if tree.number_of_nodes() == 1:
        return set(tree.nodes())
    
    # Choose an arbitrary root for the tree
    root = next(iter(tree.nodes()))
    
    # Create a directed tree from the undirected tree
    # This helps in identifying parent-child relationships
    directed_tree = nx.bfs_tree(tree, root)
    
    # Initialize DP tables
    # dp_include[node] = size of min dominating set of subtree rooted at node if node is included
    # dp_exclude[node] = size of min dominating set of subtree rooted at node if node is excluded
    dp_include = {}
    dp_exclude = {}
    
    # Store the actual vertices in the dominating set
    vertices_include = {}
    vertices_exclude = {}
    
    # Process nodes in post-order (from leaves to root)
    for node in reversed(list(nx.dfs_preorder_nodes(directed_tree, root))):
        children = list(directed_tree.successors(node))
        
        # Case 1: Node is included in the dominating set
        dp_include[node] = 1  # Count the node itself
        vertices_include[node] = {node}
        
        # Add the minimum dominating sets for each child's subtree
        for child in children:
            # If node is included, we can either include or exclude each child
            if dp_include[child] <= dp_exclude[child]:
                dp_include[node] += dp_include[child]
                vertices_include[node].update(vertices_include[child])
            else:
                dp_include[node] += dp_exclude[child]
                vertices_include[node].update(vertices_exclude[child])
        
        # Case 2: Node is excluded from the dominating set
        dp_exclude[node] = 0
        vertices_exclude[node] = set()
        
        # If node is excluded, all its children must be included or adjacent to included nodes
        for child in children:
            # Child must be included since parent (node) is excluded
            dp_exclude[node] += dp_include[child]
            vertices_exclude[node].update(vertices_include[child])
    
    # Return the minimum dominating set
    if dp_include[root] <= dp_exclude[root]:
        return vertices_include[root]
    else:
        return vertices_exclude[root]


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
    
    # Find a minimum edge cover in the graph
    min_edge_cover = nx.min_edge_cover(graph)
    
    # Create a subgraph using the edges from the minimum edge cover
    min_edge_graph = nx.Graph(min_edge_cover)
    
    # Initialize a set to store the approximate Dominating Set
    dominating_set = set()
    
    # Iterate over all connected components of the min_edge_graph
    for component in nx.connected_components(min_edge_graph):
        # Create a subgraph for the current connected component
        subgraph = min_edge_graph.subgraph(component)
        
        # Find a Dominating Set in the acyclic subgraph
        # Use the tree-based minimum dominating set algorithm 
        component_dominating_set = min_dominating_set_tree(subgraph)
        
        # Add the vertices from this connected component to the final Dominating Set
        dominating_set.update(component_dominating_set)
    
    # Remove redundant vertices from the candidate Dominating Set
    for vertex in list(dominating_set):  # Use list to avoid modifying the set during iteration
        if nx.dominating.is_dominating_set(graph, dominating_set - {vertex}):
            dominating_set.remove(vertex)

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