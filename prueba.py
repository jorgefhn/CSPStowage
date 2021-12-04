from constraint import *


problem = Problem()

#cells: position [y,x]

cells = [(0, 2), (3, 2), (1, 3), (2, 3), (0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1), (3, 1), (1, 2), (2, 2)] 
conts = [['1', 'S', '1'], ['2', 'S', '1'], ['3', 'S', '1'], ['4', 'R', '2'],['5', 'R', '2']]
print("Celdas:"+str(cells))




def notEqual (a,b):
	"""método que toma una lista de celdas por parámetro y comprueba que todas son diferentes"""
	if ((a[0] == b[0]) and (a[1] == b[1])):
		return False
	return True


#asignamos celdas a contenedores
for cont in conts:
	problem.addVariables(cont[0], cells) #asignamos posiciones con energía

for i in range(len(conts)):
	for j in range(i+1, len(conts)):
		if i != j:
			problem.addConstraint(notEqual,(conts[i][0],conts[j][0]))

sol = problem.getSolution()
print("\n\nSolución: "+str(sol))
