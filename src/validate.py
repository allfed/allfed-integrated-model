'''

A set of utility functions useful for plotting 

'''
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
	sys.path.append(module_path)

import matplotlib.pyplot as plt
import numpy as np

class Validator:
	def __init__(self):
		pass

	def checkConstraintsSatisfied(model,status,maximize_constraints,all_constraints,SHOW_CONSTRAINT_CHECK):
		if(SHOW_CONSTRAINT_CHECK):
			print(status)
		assert(status==1)

		constraints_dict={}
		# print(maximize_constraints)
		for c in all_constraints:
			if(SHOW_CONSTRAINT_CHECK):
				print(c)
			if(c.name in maximize_constraints):
				continue
			constraints_dict[c.name]=c.varValue

		for constraint in list(model.constraints.items()):
			if(constraint[0] in maximize_constraints):
				continue
			compare_type=0
			
			if(SHOW_CONSTRAINT_CHECK):
				print(constraint)

			splitted=str(constraint[1]).split(' = ')
			if(len(splitted)<2):
				compare_type=1
				splitted=str(constraint[1]).split(' <= ')
				if(len(splitted)<2):
					compare_type=2
					splitted=str(constraint[1]).split(' >= ')
					if(len(splitted)<2):
						print("Error! Assignment is not ==, <=, or >=")
						quit()
				# splitted=str(constraint[1]).split(' >= ')

			variable_string=splitted[0]	
			# print(variable_string)
			equation_string=splitted[1]	
			# print(equation_string)

			for var in model.variables():
				equation_string = equation_string.replace(var.name,str(constraints_dict[var.name]))
				variable_string = variable_string.replace(var.name,str(constraints_dict[var.name]))
			eq_val=eval(equation_string)
			var_val=eval(variable_string)
			if(SHOW_CONSTRAINT_CHECK):
				print('checking constraint '+\
				str(constraint[0])+' has '+str(constraint[1]))
			if(compare_type==0):
				if(SHOW_CONSTRAINT_CHECK):
					print('difference'+str(abs(eq_val- var_val)))
				assert(abs(eq_val- var_val)<1)
			if(compare_type==1):
				assert(var_val- eq_val<=1)
			if(compare_type==2):
				assert(eq_val- var_val<=1)
		print('all constraints satisfied')
