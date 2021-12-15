#versión que estamos probando
from argparse import ArgumentParser
import random
import copy
import ppaser as parser

class State:
	def __init__(self, contenedores: list = [], puerto_actual_del_barco: int = 0, mapa=None):
		self.contenedores = contenedores
		self.puerto_del_barco = puerto_actual_del_barco
		self.mapa = mapa


class Node:
	def __init__(self, state, parent=None, g=0, h=0, actions=[]):
		self.children = [] 			# lista de nodos hijos
		self.parent = parent 		# si tiene nodo padre o no
		self.g = g					# funcion de costes de operadores aplicados
		self.h = h					# funcion de evaluacion heuristica
		self.f = self.g + self.h 				# distancia del nodo al nodo inicial (ver si se puede usar)
		self.state = state			# estado que recibe por parametro
		self.actions = actions		# lista de acciones ejecutadas en los nodos anteriores

	def __str__(self):
		var = str(self.content)+"Coste: "+str(self.g)
		var += "\n"+str(parser.drawMap(self.mapa))+"\n"
		return var


class AStar:
	def __init__(self, initial_state, final_state):
		# Aqui tenemos que inicializar los nodos del estado inicial y del estado final
		self.initial_state_node = initial_state #Node(initial_state)
		self.final_state_node = final_state		#Node(final_state)
# -------------------------------------- Funciones auxiliares del algoritmo A* -----------------------------------

	def get_solution(self):
		# Aqui va el codigo del algortimo A*


		pass

	def expand(self, node):
		"""método para expandir un nodo"""
		# primero hay que ver que operadores se pueden aplicar al nodo recibido
		# Una vez sabemos que operacion se tiene que hacer hay que crear tantos nuevos nodos como veces la operacin
		# pueda ser aplicada (como podemos saber cuantas veces puede ser aplicada la operacion?)
		parent_node = node
		#Creamos el nuevo nodo
		new_node = Node(parent_node.state, parent_node)


		#crear todas las posibilidades válidas y añadirlas
		for cont in range(len(self.contenedores)):
			new_contenedores = copy.deepcopy(self.contenedores) #creamos nueva lista de contenedores para el nuevo estado

			carga = self.checkAction(self.asignados,self.contenedores) #comprueba que hacer: si cargar o descargar

			if carga:#si se puede cargar, cargamos el contenedor y creamos nuevo nodo
				#carga
				contenedor,coste,new_mapa,new_asignados = self.cargar(cont,self.mapa) #carga el contenedor

				if contenedor != self.contenedores[cont]:
					new_contenedores[cont] = contenedor#actualiza lista
					new_node = self.generateNode(new_contenedores,coste,new_asignados,new_mapa)
					self.children.append(new_node)

# -------------------------------------- Operadores --------------------------------------------------------------
	'''def cargar(self, posicion: int, mapa: list):
		"""Busca por posición y lo carga"""


		id,coste,x,y = array_contenedores[posicion][0],0,-1,-1
		contenedor,new_mapa,new_asignados = copy.deepcopy(self.contenedores[posicion]),copy.deepcopy(mapa),copy.deepcopy(self.asignados)
		
		while not self.comprobar_valido(x,y):
			x,y = random.randint(0,len(new_mapa)-1),random.randint(0,len(new_mapa[0])-1)

		
		if self.contenedores[posicion][2] != "B":
			contenedor[0], contenedor[1],contenedor[2]= x,y,"B"
			new_mapa[x][y] = str(id) #guardamos el id en la celda
			new_asignados[id] = (contenedor[0],contenedor[1])
			coste = 10 + (x+1) #coste = 10 + nº de filas 
		
		return contenedor,coste,new_mapa,new_asignados #devuelve contenedor y el coste asociado'''

	def descargar(self, posicion:int):
		"""método que coge contenedor y lo descarga de la lista de contenedores"""
		#Esto se podria hacer creando el node con los atributos de los contenedores

		contenedor = copy.deepcopy(self.contenedores[posicion])
		new_mapa = copy.deepcopy(mapa) #hace una copia
		new_asignados = copy.deepcopy(self.asignados) #copia de asignados


		x,y = contenedor[posicion][0],contenedor[posicion][1] #posiciones previamente guardadas
		contenedor[posicion][0],contenedor[posicion][1],contenedor[posicion][2] = None,None, self.puerto#desasigna su posición
		new_mapa[x][y] = self.devolver_tipo(self.contenedores[posicion]) #devolvemos a la casilla que había
		coste = 15 + 2*(x+1) #coste = 10 + nº de filas 
		return coste #devuelve el coste de descargar

	def navegar(self):
		"""operador para navegar. Se tienen que comprobar las condiciones para que navegue"""

		#faltaría hacer la comprobación de que se puede navegar
		new_contenedores = copy.deepcopy(self.contenedores)
		new_node = Node(new_contenedores,self.puerto+1,self.parent,self.start,self.goal,self.mapa)
		self.children.append(new_node)
		return 3500 #coste de navegar

# -------------------------------------- Funciones auxiliares de los operadores -----------------------------------
	'''def comprobar_valido(self, x, y):
		"""metodo auxiliar para comprobar que la posición es válida"""
		valores = list(self.asignados.values())
		return (x,y) not in valores and mapa[x][y] != "X" and ( (x < max_prof-1 and (mapa[x+1][y] == "X" or (x+1,y) in valores)) or (x == max_prof-1))'''

	'''def devolver_tipo(self, contenedor: list):
		"""método auxiliar para devolver el tipo de celda que tiene que retornar al mapa según el tipo de contenedor"""
		pos = -1

		for cont in range(len(array_contenedores)):
			if array_contenedores[cont][0] == contenedor[2]: #busca la coincidencia por el id
				pos = cont

		correspondencias = {'S':'N','R':'E'}

		return str((correspondencias[array_contenedores[pos][1]]))'''

	def checkAction(self, contenedores: list, asignados: list):
		# Hay una gerarquia de verificar las acciones
		# Primero verificamos la descarga
		# Segundo verficamos la carga
		# Tercero verficamos la navegacion
		return len(self.asignados) < len(self.contenedores)

	def generateNode(self,new_contenedores: list, coste: int, new_asignados: list, new_mapa: list):
		"""método auxiliar que genera nodo"""

		new_node = Node(new_contenedores, self.puerto, self.parent, new_mapa)
		new_node.g += coste
		new_node.asignados = new_asignados
		return new_node


# -------------------------------------- Main del programa -----------------------------------

# Aqui tenemos que tener toda la data parseada de los ficheros y jugar con
# ella para crear los estados iniciales y finales


def get_initial_state():
	# Le pasamos al constructor State la lista de contenedores correspondiente del estado inicial, el puerto actual y el
	# contendores = [[None, None, 0]] * numero_de_contenedores
	# Por cuestiones de claridad capaz seria bueno tener un array estatico que se corresponda con el array contenedores
	initial_state = State()
	return initial_state


def get_final_state():
	final_state = State()
	return final_state


contenedores = parser.devuelveContenedores()
mapa = parser.generateMap()
print(contenedores)
print(mapa)
initial_state = get_initial_state()
final_state = get_final_state()

#AStar(initial_state, final_state)
#AStar.get_solution()

"""
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


"""

