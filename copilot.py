import pandas as pd
from pulp import LpProblem, LpVariable, LpMinimize

# Define the data
power_plants = {
    'Plant1': {'capacity': 100, 'cost_per_unit': 30},
    'Plant2': {'capacity': 150, 'cost_per_unit': 25},
    'Plant3': {'capacity': 200, 'cost_per_unit': 35}
}

# Sample DataFrame representing demand trace
demand_df = pd.DataFrame({
    'Hour': range(1, 25),
    'Demand': [320, 300, 280, 270, 250, 240, 230, 220, 210, 200, 190, 180, 180, 190, 200, 220, 240, 260, 280, 290, 310, 320, 330, 340]
})

# Create a LP problem
prob = LpProblem("Least Cost Electricity Dispatch", LpMinimize)

# Create decision variables
x = {plant: LpVariable(f"{plant}_power", 0, plant_data['capacity']) for plant, plant_data in power_plants.items()}

# Add objective function
prob += sum(x[plant] * plant_data['cost_per_unit'] for plant, plant_data in power_plants.items())

# Add constraint for meeting demand for each hour
for hour, demand in demand_df[['Hour', 'Demand']].values:
    prob += sum(x.values()) >= demand, f"Hour_{hour}_Demand"

# Solve the problem
prob.solve()

# Print the solution
print("Status:", prob.status)
print("Total Cost:", prob.objective.value())
for plant, var in x.items():
    print(f"{plant}: {var.value()}")
