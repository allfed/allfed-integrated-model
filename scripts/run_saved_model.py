import pulp
from pulp import LpMaximize, LpMinimize, LpProblem, LpVariable, LpConstraint

variables, model = LpProblem.from_json("../model.json")
# Solve the model
model.solve()
status = pulp.LpStatus[model.status]
# Check the status of the solution
# Print the optimized objective function value
print(f"Objective value: {pulp.value(model.objective)}")
print("")
print("")
print("Model printout:")
print(model)
print("")
print("")
print("")
print("Status:", status)
if status != 1:
    print("Model optimization failed!")
else:
    print("Model optimization succeeded!")
