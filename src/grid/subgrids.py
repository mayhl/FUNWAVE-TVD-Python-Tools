##
# @file subgrids.py
#
# @brief Interface for FUNWAVE-TVD input/driver text file.
#
# @section description_inputfile Description
# Example Python program with Doxygen style comments.
#
# @section libraries_main Libraries/Modules
# - enum standard library (https://https://docs.python.org/3/library/enum.html)
#   - Access to enumeration functionality.
# - pandas library (https://pandasguide.readthedocs.io/en/latest/)
#   - Access to parsing CSV files.
#
# @section notes_inputfile Notes
# - Comments are Doxygen compatible.
#
# @section todo_doxygen_example TODO
# - None.
#
# @section author_doxygen_example Author(s)
# - Created by Michael-Angelo Y.-H. Lam on 04/29/2022.
#
# Copyright (c) 2022 FUNWAVE-TVD Group.  All rights reserved.

#from funwavetvdtools.error import FunException
#import funwavetvdtools.validation as fv

import numpy as np

def _get_factors(n):
    factors = []
    for i in range(1,n+1):
        j = int(n//i)
        if i*j == n: factors.append((i,j))

    return factors 


def compute_optimal(m_glob, n_glob, threads_per_node, max_nodes=20, optimal_points=150):

    def _compute_optimal_subgrid(n_nodes):
        n_procs = n_nodes*threads_per_node
        factors = _get_factors(n_procs)

        # Computing subgrids and aspect ratios 
        subgrids  = [(m_glob/PX, n_glob/PY) for PX, PY in factors]
        aspect_ratios = [max(m_loc,n_loc)/min(m_loc,n_loc) for m_loc, n_loc in subgrids]
        
        # Getting subgrid with aspect ratio closest to unity
        idx = np.argmin(aspect_ratios)
        return subgrids[idx], factors[idx]
        
    def _is_subgrid_optimal(subgrid):
        m_loc, n_loc = subgrid
        return (m_loc <= optimal_points) and (n_loc <= optimal_points)
    
    def _compute_relative_area_diff(subgrid):
        m_loc, n_loc = subgrid
        area = m_loc*n_loc
        optimal_area = optimal_points**2
        return np.abs(area - optimal_area)/optimal_area

    # Simple function to combine tuple with integer into tuple    
    def _rwrap(n_nodes, factors):
        return (n_nodes,) + factors

    # Checking if single node optimal subgrid dimensions are less 
    # than optimal numper of points
    old_n_nodes = 1
    old_subgrid, old_factors = _compute_optimal_subgrid(old_n_nodes)    
    if _is_subgrid_optimal(old_subgrid): return _rwrap(old_n_nodes, old_factors)

    # Computing optimal subgrids for increasing number of nodes 
    for n_nodes in range(2, max_nodes+1):
        subgrid, factors = _compute_optimal_subgrid(n_nodes)
        
        # Checks if new subgrid dimensions are less 
        # than optimal number of points
        if _is_subgrid_optimal(subgrid):
            # Choosing subgrid area closest to area corresponding
            # to optimal number of points  
            diff = _compute_relative_area_diff(subgrid)
            old_diff = _compute_relative_area_diff(old_subgrid)
            return _rwrap(old_n_nodes, old_factors) if old_diff < diff else _rwrap(n_nodes, factors)

        
        old_n_nodes, old_subgrid, old_factors = n_nodes, subgrid, factors 


    # Returning optimal subgrids with max number of nodes
    return _rwrap(old_n_nodes, old_factors)
        



