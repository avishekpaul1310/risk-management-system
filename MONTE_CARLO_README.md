# Monte Carlo Risk Simulation Feature

## Overview

This feature integrates Monte Carlo simulation into the Project Risk Management System to provide probabilistic cost analysis of project risks. Instead of relying on simple risk scores, this simulation estimates the potential total cost impact of all project risks using statistical modeling.

## How It Works

### Core Concept
Each risk is modeled with three cost estimates:
- **Optimistic Cost**: Best-case scenario if the risk occurs
- **Most Likely Cost**: Most probable cost if the risk occurs  
- **Pessimistic Cost**: Worst-case scenario if the risk occurs
- **Likelihood Percentage**: Probability of the risk occurring (1-100%)

### Simulation Process
1. **Risk Sampling**: For each simulation run, the system:
   - Determines if each risk occurs based on its likelihood percentage
   - If a risk occurs, samples a cost from the triangular distribution defined by the three cost estimates
   - Sums all costs for that simulation run

2. **Statistical Analysis**: After thousands of simulation runs, the system provides:
   - Mean and median total costs
   - Percentile analysis (90th, 95th percentiles)
   - Full distribution histogram
   - Min/max possible costs

## Business Value

### For Project Managers
- **Better Budgeting**: Use 90th percentile values for contingency planning
- **Risk Prioritization**: Understand which risks contribute most to cost uncertainty
- **Stakeholder Communication**: Present probabilistic cost estimates with confidence intervals

### For Executives
- **Portfolio Analysis**: Compare risk profiles across multiple projects
- **Investment Decisions**: Make informed decisions based on risk-adjusted cost projections
- **Contingency Planning**: Set appropriate reserve funds based on statistical analysis

## Technical Implementation

### Backend
- **Monte Carlo Engine**: Custom Python implementation using triangular distribution
- **Statistical Analysis**: Calculation of percentiles, mean, standard deviation
- **Data Validation**: Ensures cost estimates follow logical ordering (Optimistic ≤ Most Likely ≤ Pessimistic)

### Frontend
- **Interactive Dashboard**: Chart.js visualization of cost distribution
- **AJAX Integration**: Real-time simulation without page refresh
- **User Controls**: Configurable simulation parameters (1K-10K runs)

### Database Schema
New fields added to Risk model:
- `likelihood_percentage`: Integer (1-100)
- `optimistic_cost_impact`: Decimal field
- `most_likely_cost_impact`: Decimal field  
- `pessimistic_cost_impact`: Decimal field

## Usage Instructions

### Setting Up Risks for Simulation
1. Navigate to a project and add/edit risks
2. Fill in the Monte Carlo parameters:
   - Set likelihood percentage (e.g., 30% for a medium probability risk)
   - Enter optimistic, most likely, and pessimistic cost estimates
   - Ensure costs are in logical order

### Running Simulations
1. Go to the project detail page
2. Click "Monte Carlo Simulation" button
3. Choose number of simulation runs (5,000 recommended)
4. Click "Run Simulation"
5. View results in histogram and statistics table

### Interpreting Results
- **90th Percentile**: "There's a 90% chance total risk costs will be ≤ this amount"
- **Mean Cost**: Average expected cost across all simulations
- **Histogram**: Shows the full probability distribution of potential costs

## Example Scenario

**Project**: New Software Development
**Risks**:
1. **Technical Debt Risk**
   - Likelihood: 60%
   - Costs: $5K (optimistic), $15K (most likely), $30K (pessimistic)

2. **Resource Availability Risk**
   - Likelihood: 25%  
   - Costs: $10K (optimistic), $25K (most likely), $50K (pessimistic)

**Simulation Results** (5,000 runs):
- Mean Cost: $14,500
- 90th Percentile: $28,000
- This tells management there's a 90% chance risk costs will stay under $28K

## Benefits for Resume/Portfolio

This feature demonstrates:
- **Advanced Programming**: Statistical modeling and simulation algorithms
- **Full-Stack Development**: Backend Python + Frontend JavaScript integration
- **Data Visualization**: Interactive charts and statistical dashboards
- **Business Analytics**: Translating technical analysis into business insights
- **Risk Management Expertise**: Understanding of quantitative risk analysis methods
- **Software Architecture**: Clean separation of concerns, reusable components

## Future Enhancements

1. **Correlation Modeling**: Account for dependencies between risks
2. **Monte Carlo Scheduling**: Extend to time-based project scheduling risks
3. **Sensitivity Analysis**: Identify which risks drive the most cost variance
4. **Export Capabilities**: PDF reports and Excel export of simulation results
5. **Historical Analysis**: Compare simulated vs. actual outcomes for model improvement

## Technical Skills Demonstrated

- **Python**: Object-oriented programming, statistical algorithms
- **Django**: Model design, view logic, form validation
- **JavaScript**: AJAX, Chart.js, DOM manipulation
- **Statistics**: Probability distributions, percentile analysis
- **Database Design**: Schema evolution, migrations
- **UI/UX**: Responsive design, data visualization best practices
