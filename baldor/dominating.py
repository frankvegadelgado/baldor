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

# Example usage:
def example():
    # Create a tree with 8 nodes
    tree = nx.Graph()
    tree.add_edges_from([
        (0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), (6, 7)
    ])
    
    dominating_set = min_dominating_set_tree(tree)
    print(f"Minimum dominating set: {dominating_set}")
    print(f"Size of minimum dominating set: {len(dominating_set)}")
    
    # Verify that it's a valid dominating set
    dominated = set(dominating_set)
    for node in tree.nodes():
        if node not in dominated:
            dominated.update(tree.neighbors(node))
    
    is_valid = dominated == set(tree.nodes())
    print(f"Is valid dominating set: {is_valid}")