'''

A set of utility functions useful for plotting 

'''
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
	sys.path.append(module_path)

import matplotlib.pyplot as plt


class Validator:
	def __init__(self):
		pass

	def checkConstraintsSatisfied(model,status,maximize_constraints,SHOW_CONSTRAINT_CHECK):

		assert(status==1)

		for constraint in list(model.constraints.items()):
			if(constraint[0] in maximize_constraints):
				continue
			splitted=str(constraint[1]).split(' <= ')
			if(len(splitted)<2):
				print("Error! Assignment of form <= required")
				quit()
				# splitted=str(constraint[1]).split(' >= ')

			variable_string=splitted[0]	
			equation_string=splitted[1]	

			for var in model.variables():
				equation_string = equation_string.replace(var.name,str(var.value()))
				variable_string = variable_string.replace(var.name,str(var.value()))
			eq_val=eval(equation_string)
			var_val=eval(variable_string)
			if(SHOW_CONSTRAINT_CHECK):
				print('checking constraint '+\
				str(constraint[0])+' has '+str(constraint[1]))
				assert(abs(eq_val- var_val)<.01)
		print('all constraints satisfied')
