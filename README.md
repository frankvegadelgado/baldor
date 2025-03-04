# Baldor: Minimum Dominating Set Solver

![Honoring the Memory of Aurelio Angel Baldor de la Vega (Cuban mathematician, educator and lawyer)](docs/baldor.jpg)

This work builds upon [New Insights and Developments on the Dominating Set Problem](https://www.researchgate.net/publication/389519333_New_Insights_and_Developments_on_the_Dominating_Set_Problem).

---

# Overview of the Minimum Dominating Set (MDS)

## Definition:

A **dominating set** in a graph $G = (V, E)$ is a subset $D \subseteq V$ such that every vertex not in $D$ is adjacent to at least one vertex in $D$. The **minimum dominating set (MDS)** is the smallest possible dominating set in terms of the number of vertices.

## Key Concepts:

1. **Graph Representation**:

   - $V$: Set of vertices.
   - $E$: Set of edges connecting the vertices.

2. **Dominating Set**:

   - A set $D$ where for every vertex $v \in V$, either $v \in D$ or $v$ is adjacent to some vertex in $D$.

3. **Minimum Dominating Set**:
   - The dominating set with the smallest cardinality (i.e., the fewest number of vertices).

## Applications:

- **Network Design**: Ensuring coverage in wireless sensor networks.
- **Social Networks**: Identifying influential nodes.
- **Game Theory**: Strategies in certain types of games.
- **Biology**: Modeling protein-protein interaction networks.

## Computational Complexity:

- **NP-Hard**: Finding the minimum dominating set is computationally intensive for large graphs.
- **Approximation Algorithms**: Used to find near-optimal solutions in polynomial time.

## Algorithms:

1. **Greedy Algorithm**:

   - Iteratively selects the vertex that covers the most uncovered vertices.
   - Provides a logarithmic approximation ratio.

2. **Integer Linear Programming (ILP)**:

   - Formulates the problem as an optimization problem.
   - Solvable using ILP solvers for exact solutions, though computationally expensive.

3. **Heuristics and Metaheuristics**:
   - Genetic algorithms, simulated annealing, etc., for large-scale problems.

## Challenges:

- **Scalability**: Exact algorithms are infeasible for very large graphs.
- **Dynamic Graphs**: Maintaining a minimum dominating set in graphs that change over time.

## Research Directions:

- **Parallel Algorithms**: Leveraging multi-core processors and distributed computing.
- **Machine Learning**: Using learning-based approaches to predict dominating sets.
- **Hybrid Methods**: Combining exact and heuristic methods for better performance.

## Conclusion:

The minimum dominating set problem is a fundamental issue in graph theory with wide-ranging applications. While it is computationally challenging, various algorithms and heuristics provide practical solutions for different scenarios. Ongoing research continues to improve the efficiency and applicability of these methods.

---

## Problem Statement

Input: A Boolean Adjacency Matrix $M$.

Answer: Find a Minimum Dominating Set.

### Example Instance: 5 x 5 matrix

|        | c1  | c2  | c3  | c4  | c5  |
| ------ | --- | --- | --- | --- | --- |
| **r1** | 0   | 0   | 1   | 0   | 1   |
| **r2** | 0   | 0   | 0   | 1   | 0   |
| **r3** | 1   | 0   | 0   | 0   | 1   |
| **r4** | 0   | 1   | 0   | 0   | 0   |
| **r5** | 1   | 0   | 1   | 0   | 0   |

The input for undirected graph is typically provided in [DIMACS](http://dimacs.rutgers.edu/Challenges) format. In this way, the previous adjacency matrix is represented in a text file using the following string representation:

```
p edge 5 4
e 1 3
e 1 5
e 2 4
e 3 5
```

This represents a 5x5 matrix in DIMACS format such that each edge $(v,w)$ appears exactly once in the input file and is not repeated as $(w,v)$. In this format, every edge appears in the form of

```
e W V
```

where the fields W and V specify the endpoints of the edge while the lower-case character `e` signifies that this is an edge descriptor line.

_Example Solution:_

Dominating Set Found `1, 2`: Nodes `1` and `2` constitute an optimal solution.

---

# Approximate Dominating Set Algorithm Analysis

## Overview

This algorithm computes an approximate Dominating Set for an undirected graph in polynomial time. It leverages edge covers and dominating sets on trees to achieve a sublogarithmic approximation ratio. The implementation is carried out using the NetworkX library in Python.

## Runtime Analysis

The runtime complexity of the algorithm is analyzed as follows:

1. **Removing isolated nodes**: $O(n)$, where $n$ is the number of nodes.
2. **Finding minimum edge cover**: $O(n^3)$, using the Edmonds-Gallai decomposition.
3. **Creating subgraph**: $O(m)$, where $m$ is the number of edges in the minimum edge cover.
4. **Finding connected components**: $O(n + m)$.
5. **For each connected component**:
   - Creating subgraph: $O(n_i + m_i)$, where $n_i$ and $m_i$ are the number of nodes and edges in the component.
   - Finding the Dominating Set of the subgraph (Hint: It is a tree): $O(n_i)$.

The dominant factor in the runtime is the computation of the minimum edge cover, which has a cubic time complexity. Thus, the overall time complexity of the algorithm is $O(n^3)$.

## Correctness

The correctness of the algorithm is grounded in the following principles:

1. It correctly handles edge cases, such as empty graphs or graphs with no edges.
2. Isolated nodes are removed since they do not contribute to the Dominating Set.
3. The minimum edge cover ensures that all edges are covered.
4. Finding the minimum Dominating Set in a tree is solvable in polynomial time.
5. Each connected component is processed independently, ensuring correctness for disconnected graphs.
6. Redundant nodes in the Dominating Set are removed at the conclusion of the algorithm.

While this algorithm does not guarantee an optimal solution, it provides an approximation with a ratio of at most sublogarithmic, which is theoretically sound for the Dominating Set problem.

---

# Compile and Environment

## Prerequisites

- Python ≥ 3.10

## Installation

```bash
pip install baldor
```

## Execution

1. Clone the repository:

   ```bash
   git clone https://github.com/frankvegadelgado/baldor.git
   cd baldor
   ```

2. Run the script:

   ```bash
   solve -i ./benchmarks/testMatrix1
   ```

   utilizing the `solve` command provided by Baldor's Library to execute the Boolean adjacency matrix `baldor\benchmarks\testMatrix1`. The file `testMatrix1` represents the example described herein. We also support `.xz`, `.lzma`, `.bz2`, and `.bzip2` compressed text files.

   **Example Output:**

   ```
   testMatrix1: Dominating Set Found 1, 2
   ```

   This indicates nodes `1, 2` form a Dominating Set.

---

## Dominating Set Size

Use the `-c` flag to count the nodes in the Dominating Set:

```bash
solve -i ./benchmarks/testMatrix2 -c
```

**Output:**

```
testMatrix2: Dominating Set Size 2
```

---

# Command Options

Display help and options:

```bash
solve -h
```

**Output:**

```bash
usage: solve [-h] -i INPUTFILE [-a] [-b] [-c] [-v] [-l] [--version]

Estimating the Minimum Dominating Set with a sublogarithmic approximation ratio encoded for undirected graph in DIMACS format.

options:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputFile INPUTFILE
                        input file path
  -a, --approximation   enable comparison with another polynomial-time approximation approach within a logarithmic factor
  -b, --bruteForce      enable comparison with the exponential-time brute-force approach
  -c, --count           calculate the size of the Dominating Set
  -v, --verbose         anable verbose output
  -l, --log             enable file logging
  --version             show program's version number and exit
```

---

# Batch Execution

Batch execution allows you to solve multiple graphs within a directory consecutively.

To view available command-line options for the `batch_solve` command, use the following in your terminal or command prompt:

```bash
batch_solve -h
```

This will display the following help information:

```bash
usage: batch_solve [-h] -i INPUTDIRECTORY [-a] [-b] [-c] [-v] [-l] [--version]

Estimating the Minimum Dominating Set with a sublogarithmic approximation ratio for all undirected graphs encoded in DIMACS format and stored in a directory.

options:
  -h, --help            show this help message and exit
  -i INPUTDIRECTORY, --inputDirectory INPUTDIRECTORY
                        Input directory path
  -a, --approximation   enable comparison with another polynomial-time approximation approach within a logarithmic factor
  -b, --bruteForce      enable comparison with the exponential-time brute-force approach
  -c, --count           calculate the size of the Dominating Set
  -v, --verbose         anable verbose output
  -l, --log             enable file logging
  --version             show program's version number and exit
```

---

# Testing Application

A command-line utility named `test_solve` is provided for evaluating the Algorithm using randomly generated, large sparse matrices. It supports the following options:

```bash
usage: test_solve [-h] -d DIMENSION [-n NUM_TESTS] [-s SPARSITY] [-a] [-b] [-c] [-w] [-v] [-l] [--version]

The Baldor Testing Application using randomly generated, large sparse matrices.

options:
  -h, --help            show this help message and exit
  -d DIMENSION, --dimension DIMENSION
                        an integer specifying the dimensions of the square matrices
  -n NUM_TESTS, --num_tests NUM_TESTS
                        an integer specifying the number of tests to run
  -s SPARSITY, --sparsity SPARSITY
                        sparsity of the matrices (0.0 for dense, close to 1.0 for very sparse)
  -a, --approximation   enable comparison with another polynomial-time approximation approach within a logarithmic factor
  -b, --bruteForce      enable comparison with the exponential-time brute-force approach
  -c, --count           calculate the size of the Dominating Set
  -w, --write           write the generated random matrix to a file in the current directory
  -v, --verbose         anable verbose output
  -l, --log             enable file logging
  --version             show program's version number and exit
```

---

# Code

- Python implementation by **Frank Vega**.

---

# Complexity

```diff
+ We present a polynomial-time algorithm achieving a sublogarithmic approximation factor for MDS, providing strong evidence that P = NP by efficiently solving a computationally hard problem with near-optimal solutions.
```

---

# License

- MIT License.
