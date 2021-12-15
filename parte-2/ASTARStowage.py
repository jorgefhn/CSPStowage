#versión antigua



from argparse import ArgumentParser

from constraint import *
import sys
import random
import math
import copy
problem = Problem()
#para abrir el fichero y cargar sus argumentos




#--------------------------------------------------------




parser = ArgumentParser(description='%(prog)s is an Argument Parser demo')
parser.add_argument('carpeta', help='carpeta principal')
parser.add_argument('mapa', help='mapa') #mapa 
parser.add_argument('contenedores', help='contenedores') #lista de contenedores
#parser.add_argument('heuristica', help='tipo de heuristica') #heurística utilizada
args = parser.parse_args()

#rutas 
ruta = str(args.carpeta)+'/'
ruta_mapa =ruta+str(args.mapa)+".txt"
ruta_contenedores =ruta+str(args.contenedores)+".txt"
#heuristica = str(args.heuristica)


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

#--------------------------------------------------------


#estado: [(para todo contenedor, [x,y,puerto_actual_contenedor]), puerto_actual_barco ]
#si un contenedor está asignado, [posx,posy,puerto_actual]. Si no está asignado a ningún puerto, [None,None, B (barco)]. Si está descargado en un puerto, [None,None, puerto].

#información estática que poseen los estados: array original de contenedores [id,tipo,puerto_destino]
#información dinámica: posicion x,y de cada contenedor, puerto en el que está cada contenedor (en su defecto, en el barco), mapa de carga, puerto actual del barco

class Node:
	#deberíamos ver si tantos parámetros son útiles en nuestra implementación (o es redundante poner parent y start, uno de los dos va a ser None)
	def __init__(self,contenedores:list,puerto:int,parent,start, goal,mapa:list):
		self.children = [] #lista de nodos hijos
		self.parent = parent #si tiene nodo padre o no

		#contenido del nodo
		self.contenedores = contenedores
		self.puerto = puerto
		self.content = [self.contenedores,self.puerto] #contenido de cada nodo

		self.dist = 0 #distancia del nodo al nodo inicial (ver si se puede usar)

		if parent:
			self.path = parent.path[:] #camino hasta el nodo inicial (ver si hacer deepcopy)
			self.start = parent.start
			self.goal = parent.goal
			self.asignados = parent.asignados #lista de asignados del padre
			self.g = parent.g #coge el coste acumulado del nodo parent
			self.mapa = parent.mapa #mapa del padre


		else:
			#es el nodo inicial
			self.path = [self.content] 
			self.start = start
			self.goal = goal
			self.asignados = []
			self.g = 0 #coste acumulado = 0 al inicio
			self.mapa = mapa


	def expandir(self):
		"""método para expandir un nodo"""


		#crear todas las posibilidades válidas y añadirlas
		for cont in range(len(self.contenedores)):
			#creamos nueva lista de contenedores
			new_contenedores = copy.deepcopy(self.contenedores)
			#si se puede cargar, cargamos el contenedor y creamos nuevo nodo
			if not self.parent or len(self.asignados)  < len(self.contenedores):
				#carga
				new_mapa = copy.deepcopy(self.mapa) #creamos nueva copia del mapa
				contenedor,coste,mapa = copy.deepcopy(self.cargar(cont,new_mapa)) #carga el contenedor

				if contenedor != self.contenedores[cont]:
					new_contenedores[cont] = contenedor
					new_node = Node(new_contenedores,self.puerto,self.parent,self.start,self.goal,mapa)
					new_node.g += coste
					self.children.append(new_node)


	def cargar(self,posicion,mapa):
		"""Busca por posición y lo carga"""

		id = array_contenedores[posicion][0]
		coste = 0
		contenedor = copy.deepcopy(self.contenedores[posicion])


		x,y = -1,-1
		while not self.comprobar_valido(x,y):
			x,y = random.randint(0,len(mapa)-1),random.randint(0,len(mapa[0])-1)

		
		contenedor[0], contenedor[1]= x,y

		mapa[contenedor[0]][contenedor[1]] = str(id) #guardamos el id en la celda
		self.asignados.append((contenedor[0],contenedor[1]))

		#actualizamos el coste
		coste = 10 + (x+1) #coste = 10 + nº de filas 
		return contenedor,coste,mapa #devuelve contenedor y el coste asociado


	def descargar(self,posicion:int):
		"""método que coge contenedor y lo descarga de la lista de contenedores"""
		x,y = self.contenedores[posicion][0],self.contenedores[posicion][1] #posiciones previamente guardadas
		self.contenedores[posicion][0],self.contenedores[posicion][1],self.contenedores[posicion][2] = None,None, self.puerto#desasigna su posición
		self.mapa[x][y] = self.devolver_tipo(contenedor) #devolvemos a la casilla que había
		coste = 15 + 2*(x+1) #coste = 10 + nº de filas 
		return coste #devuelve el coste de descargar

	def navegar(self):
		"""operador para navegar. Se tienen que comprobar las condiciones para que navegue"""

		#faltaría hacer la comprobación de que se puede navegar
		new_contenedores = copy.deepcopy(self.contenedores)
		new_node = Node(new_contenedores,self.puerto+1,self.parent,self.start,self.goal,self.mapa)
		self.children.append(new_node)
		return 3500 #coste de navegar



	#métodos auxiliares
	def comprobar_valido(self,x,y):
		"""metodo auxiliar para comprobar que la posición es válida"""
		return (x,y) not in self.asignados and mapa[x][y] != "X" and ( (x < max_prof-1 and (mapa[x+1][y] == "X" or (x+1,y) in self.asignados)) or (x == max_prof-1))
		
		
	def devolver_tipo(self,contenedor:list):
		"""método auxiliar para devolver el tipo de celda que tiene que retornar al mapa según el tipo de contenedor"""
		pos = -1

		for cont in range(len(array_contenedores)):
			if array_contenedores[cont][0] == contenedor[2]: #busca la coincidencia por el id
				pos = cont

		correspondencias = {'S':'N','R':'E'}

		return str((correspondencias[array_contenedores[pos][1]]))
		


	def __str__(self):

		var = str(self.content)+"Coste: "+str(self.g)
		var += "\n"+str(drawMap(self.mapa))+"\n"
		return var

	

#--------------------------------------------------------


	

#obtenemos el puerto final
puerto_final = 0
for cont in array_contenedores:
	if int(cont[2]) > puerto_final:
		puerto_final = int(cont[2])


print("-------------------------------------------------------")


contenedores_iniciales = []
for cont in array_contenedores:
	contenedores_iniciales.append([None,None,0])#guardamos las posiciones inicializadas a None y el puerto inicial (0)


#--------------------------------------------------------




'''
preguntas:

insertar en orden se puede con un append de una lista normal, o hace falta estructura de datos?

'''


#--------------------------------------------------------

puerto_inicial = 0
nodo_inicial = Node(contenedores_iniciales,puerto_inicial,None,None,None,mapa)




print(nodo_inicial)


nodo_inicial.expandir()

for child in nodo_inicial.children:
	print(child)
print("Asignados después de expandir: ",nodo_inicial.asignados)





#print(drawMap(nodo_inicial.mapa))

nodo_final = Node(contenedores_iniciales,puerto_final,None,None,None,mapa) #contiene todos los contenedores descargados: lo mismo que en el inicial
#print("Nodo final: ",nodo_final)





'''
def funcion_heuristica(self,init_node:Node,final_node:Node):

	#debería coger la función heurística del parámetro que le pasas al fichero
	pass


def a_star(init_node:Node,final_node:Node):

	abierta = [init_node]
	cerrada = []
	exito = False


	g = 0 #coste inicial
	h = funcion_heuristica(init_node,final_node) 
	f = g + h  #función de evaluación

	while not exito and len(abierta) > 0:
		n = abierta.pop(0) #quitamos el primer nodo de la lista abierta
		if n == final_node:
			exito = True

		else:
			n.expandir()
			cerrada.append(n) #metemos n en cerrada
			for child in n.children:
				cost = g + child.dist

				if child not in abierta and child not in cerrada:
					abierta.append(child) #se inserta en orden?
					g = cost
					h = funcion_heuristica(child,final_node)
					f = g + h

				if child in abierta and cost < g:
					abierta.pop(child)

				if child in cerrada and cost < g:
					cerrada.pop(child)

	return exito

print("Nodo_inicial: ",nodo_inicial)

contenedor, coste = nodo_inicial.cargar(nodo_inicial.contenedores[0])
print("Coste: ",coste)

#lo cargamos
print("Nodo_inicial despues de cargar: ",nodo_inicial)
print("Asignados: ",nodo_inicial.asignados)

print(drawMap(nodo_inicial.mapa))


#lo descargamos
nodo_inicial.descargar(nodo_inicial.contenedores[0])
print("Asignados: ",nodo_inicial.asignados)




def prueba_a_star(init_node:Node,final_node:Node):
	abierta = [init_node]
	cerrada = []
	exito = False
	


	if not exito and len(abierta) > 0:
		n = abierta.pop(0) #quitamos el primer nodo de la lista abierta
		print("primer elemento de abierta: ",n)
		
		n.expandir() #aquí no los acaba de expandir bien
		for child in n.children:
			print("Hijos de n: ",child)
		cerrada.append(n) #metemos n en cerrada

	print(cerrada)

#print(prueba_a_star(nodo_inicial,nodo_final))

'''