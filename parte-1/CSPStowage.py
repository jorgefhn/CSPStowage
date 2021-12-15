from argparse import ArgumentParser
from constraint import *
import sys
import random
import math
problem = Problem()
#para abrir el fichero y cargar sus argumentos

#--------------------------------------------------------

parser = ArgumentParser(description='%(prog)s is an Argument Parser demo')
parser.add_argument('carpeta', help='carpeta principal')
parser.add_argument('mapa', help='mapa') #mapa 
parser.add_argument('contenedores', help='contenedores') #lista de contenedores

args = parser.parse_args()

#rutas 
ruta = str(args.carpeta)+'/'
ruta_mapa =ruta+str(args.mapa)+".txt"
ruta_contenedores =ruta+str(args.contenedores)+".txt"

#--------------------------------------------------------
#metodos auxiliares
def devuelveContenedores(contenedores:str):
	"""Método auxiliar, coge str de contenedores y los devuelve en tuplas"""
	lista_contenedores = contenedores.split('\n')
	array_contenedores = []
	for contenedor in lista_contenedores:
		array_contenedores.append(contenedor.split(' '))
	return array_contenedores

def generateMap(mapa:str):
	"""Método auxiliar que convierte el str del mapa en una matriz"""
	fila= mapa.split('\n')#los divide por filas
	max_prof = len(fila) 
	n_pilas = len(fila[0].split(' ')) #los divide por columnas
	return calculaMatriz(mapa,n_pilas,max_prof)


def calculaMatriz(mapa,n_pilas:int,max_prof:int):
	"""Método auxiliar que coge mapa, filas y columnas y te devuelve una matriz con los datos"""
	
	mapa,matriz = mapa.split(),[]
	for fila in range(max_prof):
		matriz.append([])
		for columna in range(n_pilas):
			matriz[fila].append(mapa[fila*n_pilas+columna]) 

	return matriz

def drawMap(mapa:list):
	"""Método auxiliar que imprime el mapa"""
	map = ""
	for fila in mapa:
		for columna in fila:
			map += columna+" "
		map += "\n"

	return map


#--------------------------------------------------------


#mapa
mapa = open(ruta_mapa).read()
#contenedores
contenedores = open(ruta_contenedores).read()

print("Contenedores:")
array_contenedores = devuelveContenedores(contenedores)
print(array_contenedores)


#matriz con el mapa
mapa = generateMap(mapa)
n_pilas,max_prof = len(mapa[0]), len(mapa)

print("Generamos mapa: ")
print(drawMap(mapa))


#-----------------------------------------------------

#Variables

#nuestra variable son los contendores, y le asignamos una posición [y,x]

refrigerados,normales  = [],[]


#separamos entre contenedores refrigerados y normales
for contenedor in array_contenedores:
	if contenedor[1] == "R":
		refrigerados.append(contenedor)
	if contenedor[1] == "S":
		normales.append(contenedor)

#-----------------------------------------------------
#Dominios 

#guardamos dos tipos de celdas: las que están en la base y las que no.
base, no_base = [],[]


for x in range(len(mapa)):
	for y in range(len(mapa[x])):
		if (x+1 < max_prof and mapa[x][y] != "X" and mapa[x+1][y] == "X") or (x+1 == max_prof and mapa[x][y] != "X"): 
				base.append((y,x)) #está en la base
		
		else:
			no_base.append((y,x)) #no está en la base

		

#después de hacer esta distinción de dominios, distinguimos entre celdas con y sin energía, y celdas inutilizables
base_energy,base_normal = [],[] #celdas de la base
no_base_energy,no_base_normal = [],[] #celdas que no están en la base
x_cells = []#celdas inutilizables

for x in range(len(mapa)):
	for y in range(len(mapa[x])):

		if mapa[x][y] == "E":
			if (y,x) in base:
				base_energy.append((y,x))
			else:
				no_base_energy.append((y,x))
		
		if mapa[x][y] == "N":
			if (y,x) in base:
				base_normal.append((y,x))
			else:
				no_base_normal.append((y,x))
		
		if mapa[x][y] == "X":
			x_cells.append((y,x))

#celdas usables = con energía + sin energía



#hacemos una copia de las listas para restaurarlas por si la solución es none


#celdas con energía:
energy_cells = base_energy + no_base_energy

#celdas normales:
usable_cells = base + no_base


#--------------------------------------------------------

#en este punto, se da valores de los dominios a las variables 

for r in refrigerados:
	try:
		problem.addVariables(r[0], energy_cells) #asignamos posiciones con energía

	except ValueError:
		print("Ha intentado meter un contenedor duplicado")

for n in normales:
	try:
		problem.addVariables(n[0], usable_cells) #asignamos todo tipo de soluciones
	
	except ValueError:
			print("Ha intentado meter un contenedor duplicado")

#--------------------------------------------------------
"""funciones para modelar nuestras restricciones"""


def notEqual(*args):
	for i in range(len(args)):
		for j in range(i+1,len(args)):
			if args[i] == args[j]:
				return False

	return True




def apilados(*args):
	"""método que comprueba que todos los contenedores están o en la base o encima de otro"""
	for c1 in range(len(args)):

		x = args[c1][1]
		y = args[c1][0]
		booleano = False #para este contenedor
		if x +1 <= max_prof-1 and (y,x+1) in args:
			booleano = True

		if not booleano and (x + 1 <= max_prof -1  and mapa[x][y] != "X" and  mapa[x+1][y] == "X"):
			booleano = True
			
		if not booleano:
			return False

	return True


def isLowPort(*args):
	"""comprueba que todos los contenedores están apilados de modo que los de destino puerto 1 estén arriba y los de destino puerto 2 abajo"""

	for c1 in range(len(args)):
		booleano = False #para cada contenedor
		puerto1 = array_contenedores[c1][2]
		cont1 = args[c1]

		#comprobamos por pilas
		for c2 in range(len(args)):
			puerto2 = array_contenedores[c2][2]
			cont2 = args[c2]

			if c1 != c2 and cont1[0] != cont2[0]: #distinta columna
				booleano = True

			if c1 != c2 and cont1[0] == cont2[0]: #misma columna y distinto contenedor
				
				if cont1[1] < cont2[1]: #c1 encima de c2
					if puerto1 <= puerto2: #puerto de c1 <= puerto de c2
						booleano = True

					if puerto1 >  puerto2:
						return False

	return True



#-----------------------------------------------------
#Restricciones

#las claves del diccionario son los ids de los contenedores
ids_contenedores = []
for contenedor in array_contenedores:
	ids_contenedores.append(contenedor[0])

problem.addConstraint(notEqual,ids_contenedores)#comprueba que los contenedores no tienen la misma posición asignada
problem.addConstraint(apilados,ids_contenedores) #comprueba que los contenedores están apilados
problem.addConstraint(isLowPort,ids_contenedores) #comprueba que los contenedores de puerto 2 están debajo de los de puerto 1


#-----------------------------------------------------
sol = problem.getSolution() #coge una de las soluciones
print("\n\nSolución: "+str(sol))



if sol != None:
	keys = list(sol.keys())
	for i in range(len(sol)):
		x = list(sol.values())[i][1] #nº de fila
		y = list(sol.values())[i][0] #nº de columna
		mapa[x][y] = keys[i]




#-----------------------------------------------------
#sacar el resultado por un fichero 
file = open(args.mapa+"-"+args.contenedores+".output","w")
file.write(drawMap(mapa))
file.close()
#-----------------------------------------------------
print("Asignamos posiciones aleatorias: ")
print(drawMap(mapa))


print(len(problem.getSolutions())) #coge una de las soluciones
