"""
@author: Lukasz Gajewski())

''
https://stackoverflow.com/questions/76158127/linear-relaxation-infeasible-in-python-using-pulp-but-still-get-an-objective-va
"""

import pulp
from pulp import LpMaximize, LpMinimize, LpProblem, LpVariable, LpConstraint
import pulp
from typing import Tuple


def relax_problem(
    infeasible_model: pulp.LpProblem, **solver_kwargs
) -> Tuple[pulp.LpProblem, set]:
    """Relax an infeasible LP problem and identify infeasible constraints.

    The function checks if the model is unsolved or not infeasible and tries to
    solve or print an error message accordingly. It then initializes an empty
    set to store infeasible constraints and iteratively deactivates each
    constraint to check the feasibility of the model.

    Parameters
    ----------
    infeasible_model : pulp.LpProblem
        The infeasible linear programming problem to be relaxed.
    **solver_kwargs : dict
        Keyword arguments for the solver of the linear programming problem.

    Returns
    -------
    pulp.LpProblem
        The relaxed linear programming problem.
    set
        The set of infeasible constraints.

    Other Parameters
    ----------------
    solver : pulp solver, optional
        The solver to use for the linear programming problem.
        By default, the CBC (COIN-OR Branch and Cut) solver provided by PuLP is used.

    Raises
    ------
    ValueError
        If the model is not infeasible.

    Examples
    --------
    Demonstration of function usage with dummy data.

    >>> from pulp import LpProblem, LpMaximize
    >>> prob = LpProblem("Test Problem", LpMaximize)
    >>> relax_problem(prob)
    """
    solver = solver_kwargs.pop("solver", pulp.PULP_CBC_CMD(**solver_kwargs, msg=False))

    # Check if the model is unsolved. If it's unsolved, execute the `solve`
    # method to solve the model
    if infeasible_model.status == pulp.constants.LpStatusNotSolved:
        infeasible_model.solve(solver)

    # Check if the model is infeasible
    if infeasible_model.status != pulp.constants.LpStatusInfeasible:
        print(
            "The model is not infeasible. "
            f"Model status: {pulp.LpStatus[infeasible_model.status]}."
        )
        return infeasible_model, set()

    # Initialize an empty set to store the IIS
    infeasible_constraints = set()

    # Create a new LP problem to store the modified version of the original problem
    modified_model = pulp.LpProblem("modified_model", sense=infeasible_model.sense)
    modified_model.addVariables(infeasible_model.variables())
    modified_model.setObjective(infeasible_model.objective)

    # Add lower and upper bound hard limits to the new problem for each variable
    # These constraints will serve as safety nets in case the original variable
    # was unconstrained
    variables = modified_model.variables()
    for index, variable in enumerate(variables):
        modified_model.addConstraint(variable >= -100_000)
        modified_model.addConstraint(variable <= 100_000)
        modified_model._variables[index] = variable

    # Iterate over each constraint in the original problem
    # Deactivate each constraint and check if the problem is still infeasible
    # If the problem is still infeasible, add the constraint to the IIS set
    # Otherwise, activate the constraint and move on to the next one
    for constraint_name, constraint in infeasible_model.constraints.items():
        modified_model.addConstraint(constraint, name=constraint_name)
        status = modified_model.solve(solver)
        if status == pulp.constants.LpStatusInfeasible:
            infeasible_constraints.add(constraint_name)
            modified_model.constraints.pop(constraint_name)
    return modified_model, infeasible_constraints


if __name__ == "__main__":
    variables, model = LpProblem.from_json("../model.json")
    # Solve the model
    model.solve(pulp.PULP_CBC_CMD(msg=False))
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
        print("Model optimization failed! Trying again with relaxations...")
        relaxed_prob, infeasible_constraints = relax_problem(model)
        relaxed_prob.solve(pulp.PULP_CBC_CMD(msg=False))
        lpvars = {lpvar.name: lpvar.value() for lpvar in relaxed_prob.variables()}

        print(f"{' Objective Value ':=^60}")
        print(f"Status: {pulp.LpStatus[relaxed_prob.status]}")
        print(f"Objective: {relaxed_prob.objective.value()}")
        print(f"{' Variables Values ':=^60}")
        for name, value in lpvars.items():
            print(f"{name}: {value}")

        print(f"{' Problem Constraints ':=^60}")
        for lpname, lpcons in relaxed_prob.constraints.items():
            c = _c = lpcons.__str__().replace("*", " * ")
            for name, value in lpvars.items():
                c = c.replace(name, str(value))
                c = c.replace(" = ", " == ")
            res = eval(c)
            print(f"{lpname}: {_c} -> {c} -> {res}")

        print("\n======== INFEASIBLE CONSTRAINTS ========\n")
        for idx, ic in enumerate(infeasible_constraints):
            print(str(idx + 1) + ": ", ic)
    else:
        print("Model optimization succeeded!")
