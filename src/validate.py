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

	# passing in the variables explicitly to the constraint checker here
	# ensures that the final values that are used in reports are explicitly
	# validated against all the constraints.
	def checkConstraintsSatisfied(model,status,maximize_constraints,variables,SHOW_CONSTRAINT_CHECK):
		if(SHOW_CONSTRAINT_CHECK):
			print(status)
		assert(status==1)

		constraints_dict={}
		for c in variables:
			# if("Humans_Fed_Fat" in c.name):
			# 	print(c.name)
			# 	print(c.varValue)
			if(SHOW_CONSTRAINT_CHECK):
				print(c)
			if(type(c)==type([])):
				print("list")
				continue
			if(c.name in maximize_constraints):
				continue
			constraints_dict[c.name]=c.varValue
		differences=[]
		constraintlist=list(model.constraints.items())
		for constraint in constraintlist:

			if(constraint[0] in maximize_constraints):
				differences.append(0)
				continue
			compare_type=0
			if(SHOW_CONSTRAINT_CHECK):
				pass

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
			equation_string=splitted[1]	

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
				differences.append(abs(eq_val- var_val))
			if(compare_type==1):
				assert(var_val- eq_val<=1)
				differences.append(var_val- eq_val)
			if(compare_type==2):
				assert(eq_val- var_val<=1)
				differences.append(eq_val- var_val)

		print('all constraints satisfied')
		m=max(differences)
		print('biggest difference:'+str(m))
		max_index=np.where(np.array(differences)==m)[0][0]
		print('for constraint:')
		print(constraintlist[max_index])
