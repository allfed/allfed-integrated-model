# first, import pulp
import pulp

# then, conduct initial declaration of problem
linearProblem = pulp.LpProblem("Maximizing for first objective", pulp.LpMaximize)

# delcare optimization variables, using pulp
x1 = pulp.LpVariable("x1", lowBound=0)
x2 = pulp.LpVariable("x2", lowBound=0)

# add (first) objective function to the linear problem statement
linearProblem += 2 * x1 + 3 * x2

# add the constraints to the problem
linearProblem += x1 + x2 <= 10
linearProblem += 2 * x1 + x2 <= 15

# solve with default solver, maximizing the first objective
solution = linearProblem.solve()

# output information if optimum was found, what the maximal objective value is and what
# the optimal point is
print(
    str(pulp.LpStatus[solution])
    + " ; max value = "
    + str(pulp.value(linearProblem.objective))
)
