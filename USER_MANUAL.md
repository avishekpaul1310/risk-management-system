# 📚 User Manual: Risk Management System

> **Complete guide to using the Risk Management System effectively**

## 🎯 Table of Contents

1. [Getting Started](#getting-started)
2. [Managing Projects](#managing-projects)
3. [Working with Risks](#working-with-risks)
4. [Monte Carlo Simulation](#monte-carlo-simulation)
5. [User Roles and Permissions](#user-roles-and-permissions)
6. [Reports and Analytics](#reports-and-analytics)
7. [Best Practices](#best-practices)
8. [Frequently Asked Questions](#frequently-asked-questions)

## 🚀 Getting Started

### First Login

After installation, access the system at `http://127.0.0.1:8000`:

1. **Create Account**: Click "Sign Up" if you're a new user
2. **Login**: Use your credentials to access the system
3. **Dashboard**: You'll see the main dashboard with project overview

### Understanding the Interface

- **Navigation Bar**: Quick access to main functions
- **Dashboard**: Overview of all projects and risk statistics
- **Breadcrumbs**: Shows your current location in the system
- **Action Buttons**: Blue buttons for primary actions, colored buttons for specific functions

## 📁 Managing Projects

### Creating a New Project

1. **Navigate**: Click "Add Project" from the home page
2. **Fill Details**:
   - **Project Name**: Choose a clear, descriptive name
   - **Description**: Detailed project overview (optional)
3. **Save**: Click "Create Project"

### Viewing Project Details

1. **Access**: Click on any project name from the home page
2. **Overview**: See project summary, risk statistics, and risk list
3. **Actions Available**:
   - Edit project details
   - Add new risks
   - Run Monte Carlo simulation
   - Delete project (if authorized)

### Project Statistics

The project detail page shows:
- **Risk Levels**: High, Medium, Low risk counts
- **Risk Status**: Open, Mitigated, Closed counts
- **Visual Progress Bar**: Color-coded risk distribution

## 🎯 Working with Risks

### Adding a New Risk

1. **Navigate**: Go to project detail page → Click "Add Risk"
2. **Basic Information**:
   - **Risk Title**: Short, descriptive name
   - **Description**: Detailed explanation of the risk
   - **Category**: Select from Technical, Financial, Operational, Legal
   - **Owner**: Person responsible for monitoring this risk
   - **Status**: Open, Mitigated, or Closed

3. **Traditional Risk Assessment**:
   - **Likelihood**: Low (1), Medium (2), High (3)
   - **Impact**: Low (1), Medium (2), High (3)
   - **Risk Score**: Automatically calculated (Likelihood × Impact)

4. **Monte Carlo Parameters** ⭐:
   - **Likelihood Percentage**: Probability of occurrence (1-100%)
   - **Optimistic Cost**: Best-case scenario cost if risk occurs
   - **Most Likely Cost**: Expected cost if risk occurs
   - **Pessimistic Cost**: Worst-case scenario cost if risk occurs

### Risk Assessment Guidelines

#### Traditional Scoring
- **Low Impact (1)**: Minor delays, small cost increases
- **Medium Impact (2)**: Moderate delays, significant cost increases
- **High Impact (3)**: Major delays, substantial cost increases

#### Monte Carlo Cost Estimation
- **Be Realistic**: Base estimates on historical data when possible
- **Consider Range**: Ensure pessimistic is significantly higher than optimistic
- **Validate Logic**: Optimistic ≤ Most Likely ≤ Pessimistic
- **Include All Costs**: Direct costs, indirect costs, opportunity costs

### Editing Risks

1. **Access**: Click "Edit" next to any risk
2. **Make Changes**: Update any field as needed
3. **Change Comment**: Describe what changed and why
4. **Save**: Changes are automatically tracked in risk history

### Risk Responses

For each risk, you can add multiple response strategies:

1. **Navigate**: Risk detail page → "Add Response"
2. **Response Types**:
   - **Avoid**: Eliminate the risk entirely
   - **Transfer**: Move risk to third party (insurance, contracts)
   - **Mitigate**: Reduce likelihood or impact
   - **Accept**: Acknowledge and monitor the risk

3. **Response Details**:
   - **Description**: Specific actions to be taken
   - **Cost Estimate**: Budget required for response
   - **Responsible Person**: Who will execute the response
   - **Target Date**: When response should be completed
   - **Status**: Planned, In Progress, Completed

## 🎲 Monte Carlo Simulation

### Understanding Monte Carlo Simulation

**What it does**: Runs thousands of "what-if" scenarios to understand the range of possible total cost impacts from all project risks.

**Why it's valuable**: Instead of getting a single number, you get a probability distribution showing the likelihood of different cost outcomes.

### Running a Simulation

1. **Prerequisites**: Ensure all risks have Monte Carlo parameters filled in
2. **Access**: Project detail page → "Monte Carlo Simulation"
3. **Set Parameters**:
   - **Number of Simulations**: 5,000 is recommended (more = more accurate, but slower)
4. **Run**: Click "Run Simulation"
5. **Wait**: Processing may take 10-30 seconds depending on complexity

### Interpreting Results

#### Key Statistics

- **Mean Cost**: Average total cost across all simulations
- **Median Cost**: Middle value when all results are sorted
- **90th Percentile**: 90% of simulations had costs below this amount
- **95th Percentile**: 95% of simulations had costs below this amount
- **Standard Deviation**: Measure of cost variability

#### Using the Results

**For Budget Planning**:
- Use **90th Percentile** for contingency reserves
- This means 90% chance actual costs will be below this amount

**For Decision Making**:
- Compare **mean cost** vs. project budget
- If 90th percentile exceeds available budget, consider risk mitigation

**For Stakeholder Communication**:
- Show the **histogram** to illustrate cost uncertainty
- Explain that this represents thousands of possible scenarios

#### The Histogram Chart

- **X-axis**: Total cost ranges
- **Y-axis**: Number of simulations that fell in each range
- **Shape**: 
  - Normal distribution = balanced risk profile
  - Right-skewed = potential for high-cost outliers
  - Left-skewed = most scenarios are higher cost

### Simulation Best Practices

1. **Validate Inputs**: Ensure all cost estimates are realistic
2. **Regular Updates**: Re-run simulations as risks change
3. **Compare Scenarios**: Run simulations before/after mitigation
4. **Document Assumptions**: Note what estimates are based on

## 👥 User Roles and Permissions

### Role Types

1. **Viewer**: Can view projects and risks, cannot edit
2. **Contributor**: Can add and edit risks, responses
3. **Manager**: Can create projects, manage team access
4. **Administrator**: Full system access, user management

### Managing Your Profile

1. **Access**: Click your name in top navigation → "Profile"
2. **Edit**: Update role and project assignments
3. **Project Access**: Select which projects you can access

## 📊 Reports and Analytics

### Dashboard Analytics

The main dashboard provides:
- **Project Overview**: Total projects and their status
- **Risk Distribution**: Breakdown by risk level
- **Recent Activity**: Latest risk changes

### Exporting Data

1. **CSV Export**: Available on dashboard and project pages
2. **Risk Reports**: Detailed risk information in spreadsheet format
3. **Simulation Results**: Export statistical analysis for external use

### Risk History

Every risk maintains a complete history:
- **Change Log**: What changed and when
- **User Attribution**: Who made each change
- **Comments**: Explanations for changes

## 🎯 Best Practices

### Risk Identification

1. **Be Comprehensive**: Consider all risk categories
2. **Involve Team**: Get input from different perspectives
3. **Regular Reviews**: Update risk register frequently
4. **Use Templates**: Develop standard risk categories for your organization

### Cost Estimation

1. **Use Historical Data**: Base estimates on past projects
2. **Expert Judgment**: Consult with subject matter experts
3. **Document Assumptions**: Record basis for estimates
4. **Validate Ranges**: Ensure realistic spread between optimistic and pessimistic

### Simulation Usage

1. **Baseline First**: Run initial simulation with all risks
2. **Test Scenarios**: Compare with/without mitigation strategies
3. **Monitor Trends**: Track how simulations change over time
4. **Communicate Results**: Share insights with stakeholders

### Team Collaboration

1. **Assign Owners**: Every risk should have a responsible person
2. **Regular Updates**: Schedule periodic risk reviews
3. **Action Items**: Convert simulation insights into concrete actions
4. **Lessons Learned**: Document outcomes for future projects

## ❓ Frequently Asked Questions

### General Usage

**Q: How often should I update risks?**
A: Review and update risks at least weekly for active projects, or whenever project circumstances change significantly.

**Q: What if I don't have good cost estimates?**
A: Start with rough estimates and refine them over time. It's better to have approximate estimates than none at all.

**Q: Can I delete risks?**
A: Yes, but consider changing status to "Closed" instead to maintain historical records.

### Monte Carlo Simulation

**Q: How many simulations should I run?**
A: 5,000 is usually sufficient for accurate results. You can use fewer (1,000) for quick analysis or more (10,000) for maximum precision.

**Q: What if my results seem unrealistic?**
A: Check your cost estimates and likelihood percentages. Ensure they're based on realistic scenarios and historical data.

**Q: Should I use the mean or 90th percentile for budgeting?**
A: Use the 90th percentile for contingency planning - this gives you 90% confidence that costs won't exceed this amount.

### Technical Issues

**Q: The simulation is taking too long**
A: Try reducing the number of simulations or check if you have many risks with very large cost ranges.

**Q: I can't see the Monte Carlo fields**
A: Make sure you're using the updated risk forms and that the database migrations have been applied.

**Q: The chart isn't displaying**
A: Ensure JavaScript is enabled in your browser and try refreshing the page.

## 📞 Support

For additional help:
1. Check the error messages carefully
2. Review this user manual
3. Contact your system administrator
4. Refer to the technical documentation

---

*This manual covers the core functionality of the Risk Management System. For technical details and advanced configuration, see the main README.md file.*
