# versión que estamos probando


from argparse import ArgumentParser
from heuristicas import h1
import random
import math
import copy
import time
import subprocess
import sys

# para abrir el fichero y cargar sus argumentos


# --------------------------------------------------------


parser = ArgumentParser(description='%(prog)s is an Argument Parser demo')
parser.add_argument('carpeta', help='carpeta principal')
parser.add_argument('mapa', help='mapa')  # mapa
parser.add_argument('contenedores', help='contenedores')  # lista de contenedores
parser.add_argument('heuristica', help='tipo de heuristica')  # heurística utilizada
args = parser.parse_args()

# rutas
ruta = str(args.carpeta) + '/'
ruta_mapa = ruta + str(args.mapa) + ".txt"
ruta_contenedores = ruta + str(args.contenedores) + ".txt"


# heuristica = str(args.heuristica)


# --------------------------------------------------------
# metodos auxiliares
def devuelveContenedores(contenedores: str):
    """Método auxiliar, coge str de contenedores y los devuelve en tuplas"""
    lista_contenedores = contenedores.split('\n')
    array_contenedores = []
    for contenedor in lista_contenedores:
        array_contenedores.append(contenedor.split(' '))
    return array_contenedores


def generateMap(mapa: str):
    """Método auxiliar que convierte el str del mapa en una matriz"""
    fila = mapa.split('\n')  # los divide por filas
    max_prof = len(fila)
    n_pilas = len(fila[0].split(' '))  # los divide por columnas
    return calculaMatriz(mapa, n_pilas, max_prof)


def calculaMatriz(mapa, n_pilas: int, max_prof: int):
    """Método auxiliar que coge mapa, filas y columnas y te devuelve una matriz con los datos"""

    mapa, matriz = mapa.split(), []
    for fila in range(max_prof):
        matriz.append([])
        for columna in range(n_pilas):
            matriz[fila].append(mapa[fila * n_pilas + columna])

    return matriz


def drawMap(mapa: list):
    """Método auxiliar que imprime el mapa"""
    map = ""
    for fila in mapa:
        for columna in fila:
            map += columna + " "
        map += "\n"

    return map


# --------------------------------------------------------

# mapa
mapa = open(ruta_mapa).read()
# contenedores
contenedores = open(ruta_contenedores).read()

print("Contenedores:")
array_contenedores = devuelveContenedores(contenedores)
print(array_contenedores)

# matriz con el mapa
mapa = generateMap(mapa)
n_pilas, max_prof = len(mapa[0]), len(mapa)

print("Generamos mapa: ")
print(drawMap(mapa))


# --------------------------------------------------------


class AVLTree(object):

    # Function to insert a node
    def insert_node(self, root, key, content):

        # Find the correct location and insert the node
        if not root:
            return TreeNode(key, content)
        elif key < root.key:
            root.left = self.insert_node(root.left, key, content)
        else:
            root.right = self.insert_node(root.right, key, content)

        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        # Update the balance factor and balance the tree
        balanceFactor = self.getBalance(root)

        print("Balance factor: ", balanceFactor)
        if balanceFactor > 1:
            if key < root.left.key:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)

        if balanceFactor < -1:
            if key > root.right.key:
                return self.leftRotate(root)
            else:

                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)

        return root

    # Function to delete a node

    def search_node(self, root, key):
        """ Busca recursivamente un nodo"""

        if key == root.key:
            print("Éxito")
            return True


        elif key < root.key:
            root.left = self.search_node(root.left, key)

        elif key > root.key:
            root.right = self.search_node(root.right, key)

    def delete_node(self, root, key):

        # Find the node to be deleted and remove it
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete_node(root.left, key)
        elif key > root.key:
            root.right = self.delete_node(root.right, key)

        # esto se queda igual

        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.getMinValueNode(root.right)
            root.key = temp.key
            root.right = self.delete_node(root.right,
                                          temp.key)
        if root is None:
            return root

        # Update the balance factor of nodes
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balanceFactor = self.getBalance(root)

        # Balance the tree
        if balanceFactor > 1:
            if self.getBalance(root.left) >= 0:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)
        if balanceFactor < -1:
            if self.getBalance(root.right) <= 0:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)
        return root

    # Function to perform left rotation
    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    # Function to perform right rotation
    def rightRotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    # Get the height of the node
    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    # Get balance factore of the node
    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)

    def preOrder(self, root):
        if not root:
            return
        print("{0} ".format(root.key), end="")
        self.preOrder(root.left)
        self.preOrder(root.right)

    # Print the tree
    def printHelper(self, currPtr, indent, last):
        if currPtr is not None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            print(currPtr.key)
            self.printHelper(currPtr.left, indent, False)
            self.printHelper(currPtr.right, indent, True)


# estado: [(para todo contenedor, [x,y,puerto_actual_contenedor]), puerto_actual_barco ]
# si un contenedor está asignado, [posx,posy,puerto_actual]. Si no está asignado a ningún puerto, [None,None, B (barco)]. Si está descargado en un puerto, [None,None, puerto].

# información estática que poseen los estados: array original de contenedores [id,tipo,puerto_destino]
# información dinámica: posicion x,y de cada contenedor, puerto en el que está cada contenedor (en su defecto, en el barco), mapa de carga, puerto actual del barco

class State:
    def __init__(self, contenedores: list, puerto_actual_del_barco: int, mapa: list):
        self.contenedores = contenedores
        self.puerto_del_barco = puerto_actual_del_barco
        self.mapa = mapa
        self.asignados = {}

    # self.posibilidades = [] #lista de posibilidades

    def __str__(self):
        var = str(self.contenedores) + "\n"
        var += str(drawMap(self.mapa)) + "\n"
        var += str(self.asignados)
        var += "\nPuerto del barco: " + str(self.puerto_del_barco) + "\n"
        return var


class Node:

    def __init__(self, state, parent=None, g=0, h=0, actions=[]):
        self.children = []  # lista de nodos hijos
        self.parent = parent  # si tiene nodo padre o no
        self.g = g  # funcion de costes de operadores aplicados
        self.h = h  # funcion de evaluacion heuristica
        self.f = self.g + self.h  # distancia del nodo al nodo inicial (ver si se puede usar)
        self.actions = actions
        self.state = state

        if parent:
            self.path = parent.path

        else:
            self.path = []

    def expandir(self):

        # crear todas las posibilidades válidas y añadirlas
        posibles_coordenadas = self.generateCoordinates()  # genera las posibles coordenadas

        if self.checkNavigate():
            new_node = self.generateNode(self.state.contenedores, self.g + 3500, self.state.asignados, self.state.mapa,
                                         self.state.puerto_del_barco + 1)  # generamos nuevo nodo
            self.children.append(new_node)  # añade a children

        for cont in range(len(self.state.contenedores)):

            action = self.checkAction(cont)  # comprueba que hacer: si cargar o descargar

            coste, contenedor, new_mapa, new_asignados = self.generateParams(cont)[1:]

            if action == "descarga":  # hay que descargar
                # checkear si tiene contenedores desordenados
                new_contenedores = copy.deepcopy(
                    self.state.contenedores)  # creamos nueva lista de contenedores para el nuevo estado
                new_node = self.generateNode(new_contenedores, coste, new_asignados, new_mapa,
                                             self.state.puerto_del_barco)  # generamos un nuevo nodo

                x, y = new_node.state.contenedores[cont][0], new_node.state.contenedores[cont][1]
                cont_nuevo = new_node.checkReordenate(cont, x, y)
                x_nuevo, y_nuevo = new_node.state.contenedores[cont_nuevo][0], new_node.state.contenedores[cont_nuevo][
                    1]

                new_node.descargar(cont_nuevo)
                self.checkDifferent(new_node, new_contenedores, cont_nuevo)

            if action == "carga":

                for pos in posibles_coordenadas:  # por cada posible combinación
                    x, y = pos[0], pos[1]
                    new_contenedores = copy.deepcopy(
                        self.state.contenedores)  # creamos nueva lista de contenedores para el nuevo estado
                    coste, contenedor, new_mapa, new_asignados = self.generateParams(cont)[1:]

                    new_node = self.generateNode(new_contenedores, coste, new_asignados, new_mapa,
                                                 self.state.puerto_del_barco)  # generamos un nuevo nodo
                    new_node.cargar(cont, x, y)
                    self.checkDifferent(new_node, new_contenedores, cont)

    # métodos que comprueban la acción a realizar

    def checkAction(self, cont: int):
        puerto_contenedor = self.state.contenedores[cont][2]
        puerto_destino = int(array_contenedores[cont][2])

        if (puerto_contenedor == "B" and puerto_destino == self.state.puerto_del_barco):
            return "descarga"

        if (
                puerto_contenedor != "B" and puerto_destino > puerto_contenedor and puerto_destino > self.state.puerto_del_barco):  # !=
            return "carga"

        return None

    def checkNavigate(self):
        """método para comprobar si tiene que navegar"""
        for c in range(
                len(self.state.contenedores)):  # recorre todos los contenedores y comprueba si están cargados/descargados

            puerto_contenedor = self.state.contenedores[c][2]
            puerto_destino = int(array_contenedores[c][2])

            # queda contenedor por descargar/cargar
            if self.checkAction(c):  # quedan contenedores por descargar
                return False

        return True  # tiene que navegar, todos están en el barco

    def checkDifferent(self, new_node, new_contenedores: list, cont: int):

        if new_contenedores[cont] != self.state.contenedores[cont] and new_node not in self.path:
            self.children.append(new_node)  # añade el nodo a los hijos
            # new_node.path = self.path
            new_node.path.append(self)

        # new_node.path = self.path
        # new_node.path.append(self)

    def checkReordenate(self, posicion: int, x: int, y: int):

        for fila in range(0, x):  # itera sobre toda la pila

            if self.state.mapa[fila][y] not in ("N", "E", "X"):  # es una posición asignada

                pos_comparar = self.state.contenedores.index(
                    [fila, y, "B"])  # buscamos la posición en el array de cotnenedores

                return pos_comparar

        return posicion  # no tiene que reordenar

    def cargar(self, posicion: int, x: int, y: int):
        """Busca por posición y lo carga"""
        id = array_contenedores[posicion][0]  # cogemos el id del contenedor

        if self.state.contenedores[posicion][2] != "B" and self.comprobar_no_asignado(x,
                                                                                      y) and self.contenedor_compatible(
                posicion, x, y):
            self.state.contenedores[posicion] = [x, y, "B"]
            self.state.mapa[x][y] = str(id)  # guardamos el id en la celda
            self.state.asignados[id] = (x, y)
            self.g += 10 + (x + 1)  # coste = 10 + nº de filas

    def descargar(self, posicion: int):
        """método que coge contenedor y lo descarga de la lista de contenedores"""
        id, coste, contenedor, new_mapa, new_asignados = self.generateParams(
            posicion)  # cogemos los parámetros que vamos a usar
        x, y = contenedor[0], contenedor[1]  # obtenemos las posiciones del contenedore
        coste_recolocar = 0  # por defecto

        # comprobar si tiene que reordenar

        if self.comprobar_asignado(x, y):
            self.state.contenedores[posicion] = [None, None, self.state.puerto_del_barco]  # desasigna su posición
            self.state.asignados.pop(id)  # borra el elemento de la lista de asignados
            self.state.mapa[x][y] = self.devolver_tipo(posicion)  # devolvemos a la casilla que había
            self.g += 15 + 2 * (x + 1) + coste_recolocar  # coste = 15 + nº de filas + el coste de recolocar (si lo hay)

    # métodos para generar parámetros y coordenadas

    def generateCoordinates(self):
        """método auxiliar que genera dos coordenadas aleatorias válidas"""
        coordenadas_posibles = []

        for x in range(len(self.state.mapa)):
            for y in range(len(self.state.mapa[x])):
                if self.comprobar_no_asignado(x, y):
                    coordenadas_posibles.append((x, y))

        return coordenadas_posibles

    def generateParams(self, posicion):
        """método auxiliar que genera variables en los métodos de carga y descarga"""
        id = array_contenedores[posicion][0]  # cogemos el id del contenedor
        contenedor = self.state.contenedores[posicion]
        coste = self.g  # por defecto
        new_mapa = copy.deepcopy(self.state.mapa)
        new_asignados = copy.deepcopy(self.state.asignados)

        return id, coste, contenedor, new_mapa, new_asignados

    # métodos auxiliares para comprobar las posiciones de los contenedores

    def comprobar_no_asignado(self, x, y):
        """metodo auxiliar para comprobar que la posición no está asignada"""
        valores = list(self.state.asignados.values())
        return (x, y) not in valores and mapa[x][y] != "X" and (
                    (x < max_prof - 1 and (mapa[x + 1][y] == "X" or (x + 1, y) in valores)) or (x == max_prof - 1))

    def comprobar_asignado(self, x, y):
        """metodo auxiliar para comprobar que la posición está asignada"""
        valores = list(self.state.asignados.values())

        return ((x, y) in valores and mapa[x][y] != "X" and (
        (x < max_prof - 1 and (mapa[x + 1][y] == "X" or (x + 1, y) in valores))) or (
                            x == max_prof - 1))  # esta comprobación no funciona

    def devolver_tipo(self, posicion: int):
        """método auxiliar para devolver el tipo de celda que tiene que retornar al mapa según el tipo de contenedor"""
        correspondencias = {'S': 'N', 'R': 'E'}
        return str((correspondencias[array_contenedores[posicion][1]]))

    def contenedor_compatible(self, posicion, x, y):
        contenedor = array_contenedores[posicion]

        if (contenedor[1] == "R" and self.state.mapa[x][y] == "E") or (
                contenedor[1] == "S" and self.state.mapa[x][y] in ("E", "N")):
            return True

        return False

    # metodo que crea nodos

    def generateNode(self, new_contenedores: list, coste: int, new_asignados: list, new_mapa: list, new_puerto):
        """método auxiliar que genera nodo"""
        new_state = State(new_contenedores, new_puerto, new_mapa)
        new_state.asignados = new_asignados

        new_node = Node(new_state, self)
        new_node.g += coste
        return new_node

    # método que devuelve un mapa con los puertos
    def retornaPuertos(self):
        """método auxiliar que coge los puertos de una matriz"""
        mapa = copy.deepcopy(self.state.mapa)

        for fila in range(len(mapa)):
            for columna in range((len(mapa[fila]))):
                if mapa[fila][columna] not in ("X", "E", "N"):
                    # busca el id
                    position = self.state.contenedores.index([fila, columna, "B"])  # busca la posición
                    mapa[fila][columna] = int(array_contenedores[position][2])

                if mapa[fila][columna] in ("X", "E", "N"):
                    mapa[fila][columna] = -1

        return (mapa)

    # métodos propios del nodo
    def __str__(self):
        var = str(self.state) + "\nCoste: " + str(self.g) + "\n"
        return var

    def __eq__(self, other):
        return self.state.contenedores == other.state.contenedores and self.state.puerto_del_barco == other.state.puerto_del_barco


class TreeNode(Node):
    def __init__(self, key, content):
        self.key = key
        self.content = content
        self.left = None
        self.right = None
        self.height = 1

    def __str__(self):
        return str(self.content)

    def __eq__(self, other):
        return self.key == other.key


class AStar():
    def __init__(self, node_inicial, node_final):
        self.abierta = AVLTree()
        self.cerrada = AVLTree()
        self.node_inicial = node_inicial
        self.node_final = node_final

    def busqueda(self):

        """método de búsqueda de A*"""

        exito = False
        root = None
        root = self.abierta.insert_node(root, self.node_inicial.f, self.node_inicial)

        while root is not None or not exito:

            root = self.abierta.getMinValueNode(root)  # devuelve Nodo
            self.abierta.delete_node(root, root.key)  # quita el primer nodo de abierta

            print("Abierta: ")
            self.abierta.printHelper(root, "", True)

            print(root)

            if root.content == self.node_final:
                exito = True
                # verificar si hay que expandir el nodo una vez es el nodo final

            if not exito:
                root.content.expandir()

                if root is not None:
                    print("Self.cerrada: ")
                    self.cerrada.printHelper(root, "", True)

                    self.cerrada.insert_node(root, root.content.f, root.content)

                for child in root.content.children:
                    print(child)
                    new_t_node = None
                    new_t_node = self.abierta.insert_node(new_t_node, child.f, child)

        if exito:
            solucion = n.path
            return solucion

        return ("Fracaso")


# --------------------------------------------------------


# obtenemos el puerto final
puerto_final = 0
for cont in array_contenedores:
    if int(cont[2]) > puerto_final:
        puerto_final = int(cont[2])

print("-------------------------------------------------------")

contenedores_iniciales = []
contenedores_finales = []
for cont in array_contenedores:
    contenedores_iniciales.append([None, None, 0])
    contenedores_finales.append([None, None, int(cont[2])])

# --------------------------------------------------------

puerto_inicial = 0
estado_inicial = State(contenedores_iniciales, puerto_inicial, mapa)  # estado inicial
estado_final = State(contenedores_finales, puerto_final, mapa)

nodo_inicial = Node(estado_inicial)
nodo_final = Node(estado_final)
# print(nodo_inicial)


# print("Nodo final: ",nodo_final)


print("-----------------------------------------------")
print("-----------------------------------------------")
print("-----------------------------------------------")
print("-----------------------------------------------")

a_star = AStar(nodo_inicial, nodo_final)
print(a_star.busqueda())

'''


abierta = [nodo_inicial]
n = Node(estado_inicial)

final = ""


nodos_expandidos = 0
exito = False
t_inicio = time.time()

while exito is not True and len(abierta) > 0:

	n = abierta.pop(0) #quita el primero
	n.expandir()
	nodos_expandidos += 1

	for child in n.children:
		if child == nodo_final:
			final = child
			exito = True


		if child not in abierta:
			abierta.append(child)

		print(child)
		print("Retorna puertos: ")
		print(child.retornaPuertos())
		print(h1(child.retornaPuertos(),child.state.puerto_del_barco))
		print("-----------------------------------------------")




t_final = time.time()

if exito: 
	print("Has alcanzado el nodo final!!!!!")
	print("Nodos expandidos: ",nodos_expandidos)
	for nodo in final.path:
		print(nodo)
else:
	print("Fracaso")

'''

# --------------------------------------------------------
# sacar el resultado por un fichero
file = open(args.mapa + "-" + args.contenedores + "-" + args.heuristica + ".output", "w")
file.write("Tiempo total: " + str(t_final - t_inicio))
file.write("\nCoste total: " + str(final.g))
file.write("\nLongitud del plan: ")
file.write("\nNodos expandidos: " + str(nodos_expandidos))

file.close()




