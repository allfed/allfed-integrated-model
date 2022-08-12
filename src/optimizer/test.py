
import pulp
# Instantiate our problem class
model = pulp.LpProblem("Profit maximising problem", pulp.LpMaximize)

SF_Start_Month_1 = pulp.LpVariable('SF_Start_Month_1', lowBound=0)
SF_Eaten_During_Month_0 = pulp.LpVariable('SF_Eaten_During_Month_0', lowBound=0)
Humans_Fed_Kcals_0 = pulp.LpVariable('Humans_Fed_Kcals_0', lowBound=0)
Humans_Fed_Fat_0 = pulp.LpVariable('Humans_Fed_Fat_0', lowBound=0)
Humans_Fed_Protein_0 = pulp.LpVariable('Humans_Fed_Protein_0', lowBound=0)
SF_End_Month_1 = pulp.LpVariable('SF_End_Month_1', lowBound=0)
SF_Eaten_During_Month_1 = pulp.LpVariable('SF_Eaten_During_Month_1', lowBound=0)
Humans_Fed_Kcals_1 = pulp.LpVariable('Humans_Fed_Kcals_1', lowBound=0)
Humans_Fed_Fat_1 = pulp.LpVariable('Humans_Fed_Fat_1', lowBound=0)
Humans_Fed_Protein_1 = pulp.LpVariable('Humans_Fed_Protein_1', lowBound=0)

model += SF_Eaten_During_Month_0 == 116384.999415 - SF_Start_Month_1
model += Humans_Fed_Kcals_0 - 0.00308085107113*SF_Eaten_During_Month_0 == -95.048552293
model += Humans_Fed_Fat_0 - 0.00178051971814*SF_Eaten_During_Month_0 == -30.5943624157
model += Humans_Fed_Protein_0 - 0.00361676018409*SF_Eaten_During_Month_0 == -66.6045881692
model += SF_Eaten_During_Month_0 >= 73960.0
model += SF_Eaten_During_Month_0 >= 48565.55

model += Humans_Fed_Kcals_1 - 0.00308085107113*SF_Eaten_During_Month_1 == -61.6297691512
model += Humans_Fed_Fat_1 - 0.00178051971814*SF_Eaten_During_Month_1 == 59.6060132979
model += Humans_Fed_Protein_1 - 0.00361676018409*SF_Eaten_During_Month_1 == -61.6388995967
model += SF_Eaten_During_Month_1 >= 23300.47145546493379168696
model += SF_Eaten_During_Month_1 >= 47192

model += SF_Eaten_During_Month_1 ==  SF_Start_Month_1 - SF_End_Month_1



#end zero
#end 1 assigned as greater than zero

# Objective function
model += Humans_Fed_Kcals_0, "Least_fedk_0"
model += Humans_Fed_Fat_0, "Least_fedf_0"
model += Humans_Fed_Protein_0, "Least_fedp_0"
model += Humans_Fed_Kcals_1, "Least_fedk_1"
model += Humans_Fed_Fat_1, "Least_fedf_1"
model += Humans_Fed_Protein_1, "Least_fedp_1"


# Solve our problem
model.solve()
print(pulp.LpStatus[model.status])

# Print our decision variable values
print("ProductionCarA"+str(SF_Eaten_During_Month_0.varValue))

# Print our objective function value
print(pulp.value(model.objective))


# SF_Eaten_During_Month_0 = 116384.999415 - SF_Start_Month_1

# Humans_Fed_Kcals_0 - 0.00308085107113 SF_Eaten_During_Month_0 = -95.048552293

# Humans_Fed_Fat_0 - 0.00178051971814 SF_Eaten_During_Month_0 = -30.5943624157

# Humans_Fed_Protein_0 - 0.00361676018409 SF_Eaten_During_Month_0 = -66.6045881692


# 0.0169801667929 SF_Eaten_During_Month_0 >= 1255.85395833
# 0.0332618713195 SF_Eaten_During_Month_0 >= 1615.381075

# SF_Eaten_During_Month_1 = SF_Start_Month_1 - SF_End_Month_1

# Humans_Fed_Kcals_1 - 0.00308085107113 SF_Eaten_During_Month_1 = -61.6297691512

# Humans_Fed_Fat_1 - 0.00178051971814 SF_Eaten_During_Month_1 = 59.6060132979

# Humans_Fed_Protein_1 - 0.00361676018409 SF_Eaten_During_Month_1 = -61.6388995967


# 0.0169801667929 SF_Eaten_During_Month_1 >= 395.645891667

# 0.0332618713195 SF_Eaten_During_Month_1 >= 1569.71365833




# Least_Humans_Fed_Any_Month <= Humans_Fed_Kcals_0
#  Least_Humans_Fed_Any_Month <= Humans_Fed_Kcals_1
