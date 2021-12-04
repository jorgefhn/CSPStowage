from argparse import ArgumentParser
from constraint import *
import sys
import random

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
n_pilas,max_prof = len(mapa), len(mapa[0])

print("Generamos mapa: ")
print(drawMap(mapa))




#--------------------------------------------------------
"""funciones para modelar nuestras restricciones"""
def notEqual (a:list,b:list):
	"""método que toma dos celdas y devuelve si son la misma o no"""
	if ((a[0] == b[0]) and (a[1] == b[1])):
		return False
	return True

#esto está mal
def apilados(a:list,b:list):
	"""método que, si dos contenedores están en la misma pila, comprueba que no flotan"""

	#después de haber hecho la comprobación de que están en la misma pila
	ya = a[0]
	yb = b[0]

	if ya == yb:
		xa = a[1]
		xb = b[1]

		for i in range(xa,xb):
			if mapa[i][y] == "X":
				return False
	return True


def isLowPort(c1:list,c2:list):
	'''método que toma dos contenedores y devuelve si el puerto de uno es menor que el de otro'''
	return c1[2]  < c2[2]


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


#print("Refrigerados: "+str(refrigerados))
#print("Contenedores sin energía: "+str(normales))

#-----------------------------------------------------
#Dominios 

#guardamos tres arrays con los tipos de celda: con energía, normales  e inaccesibles
energy_cells,normal_cells,unusable_cells = [],[],[]

for x in range(len(mapa)):
	for y in range(len(mapa[x])):

		if mapa[x][y] == "E":
			energy_cells.append((y,x)) #asignamos a los contenedores refrigerados las celdas con energía
		
		if mapa[x][y] == "N":
			normal_cells.append((y,x)) #asignamos a los contenedores refrigerados todo tipo de celdas accesibles
		
		if mapa[x][y] == "X":
			unusable_cells.append((y,x)) #celdas inaccesibles

#celdas usables = con energía + sin energía
usable_cells = energy_cells + normal_cells


print("Energy cells: ",energy_cells)
print("Normal cells: ",normal_cells)
print("Total cells: ",usable_cells)



#en este punto, se da valores de los dominios a las variables 
for r in refrigerados:
	problem.addVariables(r[0], energy_cells) #asignamos posiciones con energía

for n in normales:
	problem.addVariables(n[0], usable_cells) #asignamos todo tipo de soluciones




#-----------------------------------------------------
#Restricciones



#los contenedores refrigerados deben estar en celdas con energía y en posiciones diferentes
for i in range(len(refrigerados)):

	for j in range(i+1, len(refrigerados)):
		if i != j:
			problem.addConstraint(notEqual,(refrigerados[i][0],refrigerados[j][0])) #tiene que comprobar de dos en dos contenedores (aridad 2)

			problem.addConstraint(apilados, (refrigerados[i][0],refrigerados[j][0])) ##tiene que comprobar de dos en dos contenedores (aridad 2)
#resto de contenedores
for i in range(len(normales)):

	for j in range(i+1, len(normales)):
		if i != j:
			problem.addConstraint(notEqual,(normales[i][0],normales[j][0])) #tiene que comprobar de dos en dos contenedores (aridad 2)
			problem.addConstraint(apilados, (normales[i][0],normales[j][0])) ##tiene que comprobar de dos en dos contenedores (aridad 2)


#-----------------------------------------------------

sol = problem.getSolution()
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
