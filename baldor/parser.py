import lzma
import bz2
import numpy as np
import networkx as nx
from . import utils

def create_graph_from_file(file):
    """Creates a NetworkX graph from a file containing a DIMACS format.

    Args:
        file: A file-like object (e.g., an opened file) containing the matrix data.

    Returns:
        A NextworkX graph the input is valid.
    """
    
    graph = nx.Graph()
    for i, line in enumerate(file):
        line = line.strip()  # Remove newline characters
        if not line.startswith('c') and not line.startswith('p'):
            edge = [np.int64(node) for node in line.split(' ') if node != 'e']
            if len(edge) != 2 or min(edge[0], edge[1]) <= 0:
                raise ValueError(f"The input file is not in the correct DIMACS format at line {i}")
            elif graph.has_edge(edge[0], edge[1]):
                raise ValueError(f"The input file contains a repeated edge at line {i}")
            else:
                graph.add_edge(edge[0], edge[1])
    return graph            

def read(filepath):
    """Reads a file and returns the corresponding undirected graph.

    Args:
        filepath: The path to the file.

    Returns:
        A NetworkX graph

    Raises:
        FileNotFoundError: If the file is not found.
    """

    try:
        extension = utils.get_extension_without_dot(filepath)
        if extension == 'xz' or extension == 'lzma':
            with lzma.open(filepath, 'rt') as file:
                graph = create_graph_from_file(file)
        elif extension == 'bz2' or extension == 'bzip2':
            with bz2.open(filepath, 'rt') as file:
                graph = create_graph_from_file(file)
        else:
            with open(filepath, 'r') as file:
                graph = create_graph_from_file(file)
        
        return graph
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")