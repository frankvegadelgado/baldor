#                   Minimum Vertex Cover Solver
#                          Frank Vega
#                      February 5th, 2025

import argparse
import time

from . import algorithm
from . import parser
from . import applogger
from . import utils


def approximation_solution(inputFile, verbose=False, log=False, count=False, bruteForce=False, approximation=False):
    """Finds an approximate vertex cover.

    Args:
        inputFile: Input file path.
        verbose: Enable verbose output.
        log: Enable file logging.
        count: Measure the size of the vertex cover.
        bruteForce: Enable brute force approach.
        approximation: Enable approximate approach within a ratio of at most 2.
    """
    logger = applogger.Logger(applogger.FileLogger() if (log) else applogger.ConsoleLogger(verbose))
    
    # Read and parse a dimacs file
    logger.info(f"Parsing the Input File started")
    started = time.time()
    
    graph = parser.read(inputFile)
    filename = utils.get_file_name(inputFile)
    logger.info(f"Parsing the Input File done in: {(time.time() - started) * 1000.0} milliseconds")
    
    logger.info("Baldor Approximate Solution started")
    started = time.time()
    
    novel_approach = algorithm.find_vertex_cover(graph)

    logger.info(f"Baldor Approximate Solution done in: {(time.time() - started) * 1000.0} milliseconds")

    answer = utils.string_result_format(novel_approach, count)
    output = f"{filename}: {answer}"
    utils.println(output, logger, log)
    
    if approximation:
        logger.info("An Approximate Solution with an approximation ratio of at most 2 started")
        started = time.time()
        
        result = algorithm.find_vertex_cover_approximation(graph)

        logger.info(f"An Approximate Solution with an approximation ratio of at most 2 done in: {(time.time() - started) * 1000.0} milliseconds")
        
        answer = utils.string_result_format(result, count)
        output = f"{filename}: (Approximation) {answer}{f" (approximate ratio Baldor vs Optimal) {2* len(novel_approach)/len(result)}" if result is not None else ""}"
        utils.println(output, logger, log)

    if bruteForce:
        logger.info("A solution with an exponential-time complexity started")
        started = time.time()
        
        result = algorithm.find_vertex_cover_brute_force(graph)

        logger.info(f"A solution with an exponential-time complexity done in: {(time.time() - started) * 1000.0} milliseconds")
        
        answer = utils.string_result_format(result, count)
        output = f"{filename}: (Brute Force) {answer}{f" (exact ratio Baldor vs Optimal) {len(novel_approach)/len(result)}" if result is not None else ""}"
        utils.println(output, logger, log)
        
        
def main():
      
    # Define the parameters
    helper = argparse.ArgumentParser(prog="solve", description='Estimating the Minimum Vertex Cover for an undirected graph encoded in DIMACS format and stored in a file.')
    helper.add_argument('-i', '--inputFile', type=str, help='input file path', required=True)
    helper.add_argument('-a', '--approximation', action='store_true', help='enable comparison with a polynomial-time approximation approach within a factor of at most 2')
    helper.add_argument('-b', '--bruteForce', action='store_true', help='enable comparison with the exponential-time brute-force approach')
    helper.add_argument('-c', '--count', action='store_true', help='calculate the size of the vertex cover')
    helper.add_argument('-v', '--verbose', action='store_true', help='anable verbose output')
    helper.add_argument('-l', '--log', action='store_true', help='enable file logging')
    helper.add_argument('--version', action='version', version='%(prog)s 0.0.1')

    # Initialize the parameters
    args = helper.parse_args()
    approximation_solution(args.inputFile, 
               verbose=args.verbose, 
               log=args.log,
               count=args.count,
               bruteForce=args.bruteForce,
               approximation=args.approximation)

if __name__ == "__main__":
    main()