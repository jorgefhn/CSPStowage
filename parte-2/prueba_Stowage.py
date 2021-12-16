#versión que estamos probando



from argparse import ArgumentParser

from constraint import *
import sys
import random
import math
import copy
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

class State:

	def __init__(self,contenedores:list,puerto:int):
		self.contenedores = contenedores
		self.puerto = puerto


	def __str__(self):
		pass



class Node:
	#deberíamos ver si tantos parámetros son útiles en nuestra implementación (o es redundante poner parent y start, uno de los dos va a ser None)
	def __init__(self,contenedores:list,puerto:int,parent,mapa:list):
		self.children = [] #lista de nodos hijos
		self.parent = parent #si tiene nodo padre o no
		self.dist = 0 #distancia del nodo al nodo inicial (ver si se puede usar)
		self.contenedores = contenedores
		self.puerto = puerto
		self.content = [self.contenedores,self.puerto]

		#contenido del nodo


		if parent:
			self.path = copy.deepcopy(parent.path) #camino hasta el nodo inicial 
			self.g = parent.g #coge el coste acumulado del nodo parent
			self.mapa = copy.deepcopy(parent.mapa) #mapa del padre


		else:
			#es el nodo inicial
			self.path = [self.content] 
			self.asignados = {}
			self.g = 0 #coste acumulado = 0 al inicio
			self.mapa = mapa



	def expandir(self):
		"""método para expandir un nodo"""


		#crear todas las posibilidades válidas y añadirlas
		for cont in range(len(self.contenedores)):
			new_contenedores = copy.deepcopy(self.contenedores) #creamos nueva lista de contenedores para el nuevo estado

			carga = self.checkAction(self.asignados,self.contenedores) #comprueba que hacer: si cargar o descargar

			if carga:#si se puede cargar, cargamos el contenedor y creamos nuevo nodo
				#carga
				print("Cargando: ")
				contenedor,coste,new_mapa,new_asignados = self.cargar(cont) #carga el contenedor

			else: #hay que descargar (o navegar)
				print("Descargando: ")
				contenedor,coste,new_mapa,new_asignados = self.descargar(cont) #carga el contenedor


			if contenedor != self.contenedores[cont]:
				new_contenedores[cont] = contenedor  # actualiza lista
				new_node = self.generateNode(new_contenedores, coste, new_asignados, new_mapa)
				self.children.append(new_node)
			

	

	def cargar(self,posicion:int):
		"""Busca por posición y lo carga"""
		id,coste,contenedor,new_mapa,new_asignados = self.generateParams(posicion)
		x,y = self.generateCoordinates() #generamos posiciones válidas

		
		if self.contenedores[posicion][2] != "B":
			contenedor = [x,y,"B"]
			new_mapa[x][y] = str(id) #guardamos el id en la celda
			new_asignados[id] = (x,y)
			coste = 10 + (x+1) #coste = 10 + nº de filas 
		
		return contenedor,coste,new_mapa,new_asignados #devuelve contenedor y el coste asociado


	def descargar(self,posicion:int):
		"""método que coge contenedor y lo descarga de la lista de contenedores"""
		id,coste,contenedor,new_mapa,new_asignados = self.generateParams(posicion)
		x,y = contenedor[0],contenedor[1]


		if self.comprobar_valido(x,y):
			contenedor = [None,None,self.puerto]#desasigna su posición
			new_asignados.pop(id) #borra el elemento de la lista de asignados
			new_mapa[x][y] = self.devolver_tipo(self.contenedores[posicion]) #devolvemos a la casilla que había
			coste = 15 + 2*(x+1) #coste = 10 + nº de filas

		return contenedor,coste,new_mapa,new_asignados #devuelve el coste de descargar


	def generateCoordinates(self):
		"""método auxiliar que genera dos coordenadas aleatorias válidas"""
		x,y = -1,-1
		while not self.comprobar_valido(x,y):
			x,y = random.randint(0,len(self.mapa)-1),random.randint(0,len(self.mapa[0])-1)#hay que comprobar cada posición válida en vez de ser aleatorio
		return x,y

	def generateCopies(self,posicion):
		"""método auxiliar usado en cargar y descargar para generar deepcopies"""
		return copy.deepcopy(self.contenedores[posicion]), copy.deepcopy(self.mapa), copy.deepcopy(self.asignados)

	def generateParams(self,posicion):
		"""método auxiliar que genera variables en los métodos de carga y descarga"""
		id = array_contenedores[posicion][0] #cogemos el id del contenedor
		coste = 0  # por defecto
		contenedor, new_mapa, new_asignados = self.generateCopies(posicion)  # generamos las copias para el nuevo nodo

		return id,coste,contenedor,new_mapa,new_asignados


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
		valores = list(self.asignados.values())
		return (x,y) not in valores and mapa[x][y] != "X" and ( (x < max_prof-1 and (mapa[x+1][y] == "X" or (x+1,y) in valores)) or (x == max_prof-1))
		
		
	def devolver_tipo(self,contenedor:list):
		"""método auxiliar para devolver el tipo de celda que tiene que retornar al mapa según el tipo de contenedor"""
		pos = -1

		for cont in range(len(array_contenedores)):
			if array_contenedores[cont][0] == contenedor[2]: #busca la coincidencia por el id
				pos = cont

		correspondencias = {'S':'N','R':'E'}

		return str((correspondencias[array_contenedores[pos][1]]))
		

	def checkAction(self,contenedores:list,asignados:list):
		return len(self.asignados) < len(self.contenedores)



	def generateNode(self,new_contenedores:list,coste:int,new_asignados:list,new_mapa:list):
		"""método auxiliar que genera nodo"""

		new_node = Node(new_contenedores,self.puerto,self.parent,new_mapa)
		new_node.g += coste
		new_node.asignados = new_asignados
		return new_node


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

puerto_inicial = 0
nodo_inicial = Node(contenedores_iniciales,puerto_inicial,None,mapa)


lista = [nodo_inicial] 
contador = 1
while len(lista) > 0:
	print("Iteracion: ",contador)
	n = lista.pop(0) #coge el primero de la lista
	n.expandir() #lo expande

	for child in n.children:

		print(child)
		lista.append(child)

	contador += 1

	print("\n")




