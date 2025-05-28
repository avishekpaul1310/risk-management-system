"""
Monte Carlo Simulation for Risk Cost Analysis
"""
import random
import math
import statistics
from decimal import Decimal
from typing import List, Dict, Any


def triangular_distribution(optimistic: float, most_likely: float, pessimistic: float) -> float:
    """
    Sample from a triangular distribution using the PERT method.
    
    Args:
        optimistic: Best-case value
        most_likely: Most probable value  
        pessimistic: Worst-case value
        
    Returns:
        Sampled value from the triangular distribution
    """
    # Ensure correct order for the distribution
    if not (optimistic <= most_likely <= pessimistic):
        raise ValueError("Optimistic must be <= Most Likely <= Pessimistic")
    
    # Pick a random number between 0 and 1
    u = random.random()
    
    # Calculate the cumulative distribution function (CDF) point for the most likely value
    # This divides the triangle into two parts based on the mode
    if pessimistic == optimistic:
        return most_likely
        
    mode_cdf = (most_likely - optimistic) / (pessimistic - optimistic)
    
    if u < mode_cdf:
        # First part of the triangle (ascending slope)
        return optimistic + math.sqrt(u * (pessimistic - optimistic) * (most_likely - optimistic))
    else:
        # Second part of the triangle (descending slope)
        return pessimistic - math.sqrt((1 - u) * (pessimistic - optimistic) * (pessimistic - most_likely))


def run_monte_carlo_simulation(risks, num_simulations: int = 5000) -> Dict[str, Any]:
    """
    Run Monte Carlo simulation for project risk costs.
    
    Args:
        risks: QuerySet of Risk objects
        num_simulations: Number of simulation iterations
        
    Returns:
        Dictionary containing simulation results and statistics
    """
    simulation_results = []
    
    # Convert Decimal fields to float for calculation
    active_risks = []
    for risk in risks.filter(status='Open'):
        active_risks.append({
            'title': risk.title,
            'likelihood_percentage': float(risk.likelihood_percentage),
            'optimistic_cost': float(risk.optimistic_cost_impact),
            'most_likely_cost': float(risk.most_likely_cost_impact),
            'pessimistic_cost': float(risk.pessimistic_cost_impact),
        })
    
    # Run simulations
    for _ in range(num_simulations):
        current_simulation_total_cost = 0
        
        for risk in active_risks:
            # Determine if the risk occurs in this simulation
            if random.random() < (risk['likelihood_percentage'] / 100.0):
                # If risk occurs, sample its cost impact using triangular distribution
                try:
                    sampled_cost_impact = triangular_distribution(
                        risk['optimistic_cost'],
                        risk['most_likely_cost'],
                        risk['pessimistic_cost']
                    )
                    current_simulation_total_cost += sampled_cost_impact
                except ValueError:
                    # If there's an issue with the distribution, use most likely value
                    current_simulation_total_cost += risk['most_likely_cost']
        
        simulation_results.append(current_simulation_total_cost)
    
    # Calculate statistics
    if not simulation_results:
        return {
            'num_simulations': num_simulations,
            'num_active_risks': len(active_risks),
            'results': [],
            'statistics': {
                'mean': 0,
                'median': 0,
                'std_dev': 0,
                'min_cost': 0,
                'max_cost': 0,
                'p10': 0,
                'p25': 0,
                'p75': 0,
                'p90': 0,
                'p95': 0,
            },
            'histogram_data': {'bins': [], 'frequencies': []}
        }
    
    sorted_results = sorted(simulation_results)
    
    statistics_data = {
        'mean': statistics.mean(simulation_results),
        'median': statistics.median(simulation_results),
        'std_dev': statistics.stdev(simulation_results) if len(simulation_results) > 1 else 0,
        'min_cost': min(simulation_results),
        'max_cost': max(simulation_results),
        'p10': sorted_results[int(0.10 * len(sorted_results))],
        'p25': sorted_results[int(0.25 * len(sorted_results))],
        'p75': sorted_results[int(0.75 * len(sorted_results))],
        'p90': sorted_results[int(0.90 * len(sorted_results))],
        'p95': sorted_results[int(0.95 * len(sorted_results))],
    }
    
    # Create histogram data for visualization
    histogram_data = create_histogram_data(simulation_results, num_bins=20)
    
    return {
        'num_simulations': num_simulations,
        'num_active_risks': len(active_risks),
        'results': simulation_results,
        'statistics': statistics_data,
        'histogram_data': histogram_data
    }


def create_histogram_data(data: List[float], num_bins: int = 20) -> Dict[str, List]:
    """
    Create histogram data for visualization.
    
    Args:
        data: List of simulation results
        num_bins: Number of histogram bins
        
    Returns:
        Dictionary with bin edges and frequencies
    """
    if not data:
        return {'bins': [], 'frequencies': []}
    
    min_val = min(data)
    max_val = max(data)
    
    if min_val == max_val:
        return {
            'bins': [min_val],
            'frequencies': [len(data)]
        }
    
    # Create bin edges
    bin_width = (max_val - min_val) / num_bins
    bin_edges = [min_val + i * bin_width for i in range(num_bins + 1)]
    
    # Count frequencies
    frequencies = [0] * num_bins
    for value in data:
        # Find which bin this value belongs to
        bin_index = min(int((value - min_val) / bin_width), num_bins - 1)
        frequencies[bin_index] += 1
    
    # Create bin labels (midpoints)
    bin_labels = []
    for i in range(num_bins):
        midpoint = (bin_edges[i] + bin_edges[i + 1]) / 2
        bin_labels.append(round(midpoint, 2))
    
    return {
        'bins': bin_labels,
        'frequencies': frequencies
    }


def format_currency(amount: float) -> str:
    """Format amount as currency string."""
    return f"${amount:,.2f}"
