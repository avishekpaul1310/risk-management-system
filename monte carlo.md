
Let's integrate a simplified Monte Carlo simulation into your Project Risk Management System. The goal is to estimate the potential total cost impact of risks, giving a probability distribution rather than just a single "risk score."

Core Idea:
Instead of a single "impact" value for each risk, you'll ask the user for an "Optimistic," "Most Likely," and "Pessimistic" cost impact. The simulation will then randomly pick an impact within that range for each risk, sum them up for the project, and repeat this many times to build a distribution of total risk costs.

Step 1: Modify Risk Input Fields (Frontend & Backend)

Current: You likely have a field for "Impact" (and "Likelihood").

New Input: For each risk, add three fields for Cost Impact:

Optimistic Cost Impact (OC): The best-case scenario if this risk occurs.
Most Likely Cost Impact (MLC): The most probable cost if this risk occurs.
Pessimistic Cost Impact (PC): The worst-case scenario cost if this risk occurs.
(Optional but recommended) Likelihood field: Still keep this, perhaps as a percentage (e.g., 10% to 100%).
Backend Changes: Update your Django risk model to store these three new cost impact values.

Step 2: Add a "Run Simulation" Feature

User Interface: Add a button on your project's risk management page, perhaps labeled "Run Cost Risk Simulation" or "Estimate Probable Risk Cost."
Parameters: You might also add an input field for the user to define the number of simulations (e.g., default to 1,000 or 5,000 runs).
Step 3: Implement the Monte Carlo Logic (Backend - Django View/Helper Function)

This is where the core calculation happens.

Retrieve Active Risks: When the simulation button is clicked, fetch all active risks associated with the current project from your database.
Define Simulation Runs: Set a number of iterations (e.g., num_simulations = 5000).
Initialize Results List: Create an empty list to store the total risk cost for each simulation run (e.g., total_project_costs = []).
Loop for Each Simulation:

import random
import math

# A simple triangular distribution sampling function
# This is a common and easy-to-understand distribution for estimates.
def triangular_dist(optimistic, most_likely, pessimistic):
    # Ensure correct order for the distribution
    if not (optimistic <= most_likely <= pessimistic):
        raise ValueError("Optimistic must be <= Most Likely <= Pessimistic")

    # Pick a random number between 0 and 1
    u = random.random()

    # Calculate the cumulative distribution function (CDF) point for the most likely value
    # This divides the triangle into two parts based on the mode
    mode_cdf = (most_likely - optimistic) / (pessimistic - optimistic)

    if u < mode_cdf:
        # First part of the triangle
        return optimistic + math.sqrt(u * (pessimistic - optimistic) * (most_likely - optimistic))
    else:
        # Second part of the triangle
        return pessimistic - math.sqrt((1 - u) * (pessimistic - optimistic) * (pessimistic - most_likely))

# --- Main simulation loop ---
simulation_results = []
num_simulations = 5000 # User configurable?

for _ in range(num_simulations):
    current_simulation_total_cost = 0
    for risk in active_risks: # Iterate through each risk from your database
        # Step 3a: Determine if the risk occurs in this simulation
        # Use random.random() < (risk.likelihood / 100) if likelihood is a percentage
        if random.random() < (risk.likelihood_percentage / 100.0): # Assuming likelihood is stored as a percentage
            # Step 3b: If risk occurs, sample its cost impact
            sampled_cost_impact = triangular_dist(
                risk.optimistic_cost_impact,
                risk.most_likely_cost_impact,
                risk.pessimistic_cost_impact
            )
            current_simulation_total_cost += sampled_cost_impact
    simulation_results.append(current_simulation_total_cost)

# simulation_results now contains 5000 possible total cost impacts

Step 4: Visualize the Results (Frontend - Dashboard)

Histogram: The most intuitive way to display Monte Carlo results is a histogram. This shows the frequency of different total cost impacts.
Use a JavaScript charting library (e.g., Chart.js, D3.js, Plotly.js - you mentioned Chart.js in your other projects, so that's a good choice).
The backend will send the simulation_results list to the frontend.
Group these results into "bins" (e.g., $0-$100, $101-$200, etc.) and count how many simulation runs fell into each bin.
Plot these bins as a bar chart (histogram).
Key Metrics:
Display the Mean/Average total risk cost.
Display a P90 (90th percentile) cost: "There's a 90% chance the total risk cost will be less than or equal to $X." This is extremely useful for setting contingency budgets. You can calculate this by sorting simulation_results and picking the value at the 90th percentile.
Display the Min and Max simulated costs.