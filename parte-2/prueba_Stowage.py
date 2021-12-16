# versión que estamos probando


from argparse import ArgumentParser

from constraint import *
import sys
import random
import math
import copy

# para abrir el fichero y cargar sus argumentos


# --------------------------------------------------------


parser = ArgumentParser(description='%(prog)s is an Argument Parser demo')
parser.add_argument('carpeta', help='carpeta principal')
parser.add_argument('mapa', help='mapa')  # mapa
parser.add_argument('contenedores', help='contenedores')  # lista de contenedores
# parser.add_argument('heuristica', help='tipo de heuristica') #heurística utilizada
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


# estado: [(para todo contenedor, [x,y,puerto_actual_contenedor]), puerto_actual_barco ]
# si un contenedor está asignado, [posx,posy,puerto_actual]. Si no está asignado a ningún puerto, [None,None, B (barco)]. Si está descargado en un puerto, [None,None, puerto].

# información estática que poseen los estados: array original de contenedores [id,tipo,puerto_destino]
# información dinámica: posicion x,y de cada contenedor, puerto en el que está cada contenedor (en su defecto, en el barco), mapa de carga, puerto actual del barco

class State:
    def __init__(self, contenedores: list, puerto_actual_del_barco: int, mapa:list):
        self.contenedores = contenedores
        self.puerto_del_barco = puerto_actual_del_barco
        self.mapa = mapa
        self.asignados = {}
        #self.posibilidades = [] #lista de posibilidades

    def __str__(self):
        var = "Contenedores: "+ str(self.contenedores)+"\n"
        var += str(drawMap(self.mapa))
        return var


class Node:
    def __init__(self, state,parent =None ,g= 0, h = 0, actions = []):
        self.children = []  # lista de nodos hijos
        self.parent = parent  # si tiene nodo padre o no
        self.g = g  # funcion de costes de operadores aplicados
        self.h = h  # funcion de evaluacion heuristica
        self.f = self.g + self.h  # distancia del nodo al nodo inicial (ver si se puede usar)
        self.actions = actions
        self.state = state

        self.contenedores = self.state.contenedores
        self.puerto = self.state.puerto_del_barco
        self.asignados = self.state.asignados
        self.mapa = self.state.mapa

        #posibles coordenadas
        self.posibles_coordenadas = self.generateCoordinates()
        #self.actions = actions  # lista de acciones ejecutadas en los nodos anteriores

    def expandir(self):
        """método para expandir un nodo"""

        # crear todas las posibilidades válidas y añadirlas
        posibles_coordenadas = self.generateCoordinates() #genera las posibles coordenadas

        for cont in range(len(self.contenedores)):
            for pos in posibles_coordenadas:

                #todo esto hay que encapsularlo
                x,y = pos[0],pos[1]
                new_contenedores = copy.deepcopy(
                    self.contenedores)  # creamos nueva lista de contenedores para el nuevo estado
                contenedor = self.contenedores[cont]
                coste = 0
                new_asignados = self.asignados
                new_mapa = self.mapa
                puerto = self.puerto

                #hasta aquí


                action = self.checkAction(self.contenedores)  # comprueba que hacer: si cargar o descargar

                if action =="carga":  # hay que cargar
                    print("Cargando: ")
                    if (x,y) not in self.asignados:
                        contenedor, coste, new_mapa, new_asignados = self.cargar(cont,x,y)  # carga el contenedor


                if action == "descarga":  # hay que descargar
                    print("Descargando: ")
                    contenedor, coste, new_mapa, new_asignados = self.descargar(cont)  # carga el contenedor

                if action == "navegación": #hay que navegar
                    print("Navegando:")
                    puerto = self.puerto +1
                    coste = self.navegar()


                # generación de nuevo nodo
                if action == "navegación" or (action in ("carga","descarga") and contenedor != self.contenedores[cont]):

                    new_contenedores[cont] = contenedor  # actualiza lista

                    self.generateNode(new_contenedores, coste, new_asignados, new_mapa,puerto)

    def cargar(self, posicion: int,x:int,y:int):
        """Busca por posición y lo carga"""
        id, coste, contenedor, new_mapa, new_asignados = self.generateParams(posicion)  # cogemos los parámetros que vamos a usar

        if self.contenedores[posicion][2] != "B":
            contenedor = [x, y, "B"]
            new_mapa[x][y] = str(id)  # guardamos el id en la celda
            new_asignados[id] = (x, y)
            coste = 10 + (x + 1)  # coste = 10 + nº de filas

        return contenedor, coste, new_mapa, new_asignados  # devuelve contenedor y el coste asociado

    def descargar(self, posicion: int):
        """método que coge contenedor y lo descarga de la lista de contenedores"""
        id, coste, contenedor, new_mapa, new_asignados = self.generateParams(
            posicion)  # cogemos los parámetros que vamos a usar
        x, y = contenedor[0], contenedor[1]  # obtenemos las posiciones del contenedore


        if self.comprobar_asignado(x, y):
            contenedor = [None, None, self.puerto]  # desasigna su posición
            new_asignados.pop(id)  # borra el elemento de la lista de asignados
            new_mapa[x][y] = self.devolver_tipo(posicion)  # devolvemos a la casilla que había
            coste = 15 + 2 * (x + 1)  # coste = 10 + nº de filas

        return contenedor, coste, new_mapa, new_asignados  # devuelve el coste de descargar

    def generateCoordinates(self):
        """método auxiliar que genera dos coordenadas aleatorias válidas"""
        coordenadas_posibles = []

        for x in range(len(self.mapa)):
            for y in range(len(self.mapa[x])):
                if self.comprobar_no_asignado(x,y):
                    coordenadas_posibles.append((x,y))

        return coordenadas_posibles

    def generateCopies(self, posicion):
        """método auxiliar usado en cargar y descargar para generar deepcopies"""
        return copy.deepcopy(self.contenedores[posicion]), copy.deepcopy(self.mapa), copy.deepcopy(self.asignados)

    def generateParams(self, posicion):
        """método auxiliar que genera variables en los métodos de carga y descarga"""
        id = array_contenedores[posicion][0]  # cogemos el id del contenedor
        coste = 0  # por defecto
        contenedor, new_mapa, new_asignados = self.generateCopies(posicion)  # generamos las copias para el nuevo nodo

        return id, coste, contenedor, new_mapa, new_asignados

    def navegar(self):
        """operador para navegar. Se tienen que comprobar las condiciones para que navegue"""

        # faltaría hacer la comprobación de que se puede navegar
        return 3500  # coste de navegar

    # métodos auxiliares

    def comprobar_no_asignado(self, x, y):
        """metodo auxiliar para comprobar que la posición no está asignada"""
        valores = list(self.asignados.values())
        return (x, y) not in valores and mapa[x][y] != "X" and (
                    (x < max_prof - 1 and (mapa[x + 1][y] == "X" or (x + 1, y) in valores)) or (x == max_prof - 1))

    def comprobar_asignado(self, x, y):
        """metodo auxiliar para comprobar que la posición está asignada"""
        valores = list(self.asignados.values())
        return (x, y) in valores and mapa[x][y] != "X" and (
                    (x < max_prof - 1 and (mapa[x + 1][y] == "X" or (x + 1, y) in valores)) or (x == max_prof - 1))

    def devolver_tipo(self, posicion: int):
        """método auxiliar para devolver el tipo de celda que tiene que retornar al mapa según el tipo de contenedor"""
        correspondencias = {'S': 'N', 'R': 'E'}
        return str((correspondencias[array_contenedores[posicion][1]]))

    def checkAction(self, contenedores: list):
        # Iteramos sobre todos los contenedores para verificar que
        # cada uno de ellos cumpla con las siguientes condiciones
        for cont in range(len(contenedores)):
            puerto_destino = array_contenedores[cont][2] #coge el puerto de destino del contenedor
            estado_contenedor = self.contenedores[cont][2] #coge el estado actual del contenedor

            if puerto_destino == self.puerto and estado_contenedor =="B":
                return "descarga"

            if estado_contenedor != "B" and puerto_destino != self.puerto:
                return "carga"

        return "navegación"






    def generateNode(self, new_contenedores: list, coste: int, new_asignados: list, new_mapa: list,new_puerto):
        """método auxiliar que genera nodo"""
        new_state = State(new_contenedores,new_puerto,new_mapa)
        new_node = Node(new_state,self)
        new_node.g += coste
        new_node.asignados = new_asignados
        self.children.append(new_node)

    def __str__(self):

        var = str(self.state)
        return var


# --------------------------------------------------------


# obtenemos el puerto final
puerto_final = 0
for cont in array_contenedores:
    if int(cont[2]) > puerto_final:
        puerto_final = int(cont[2])

print("-------------------------------------------------------")

contenedores_iniciales = []
for cont in array_contenedores:
    contenedores_iniciales.append([None, None, 0])

# --------------------------------------------------------

puerto_inicial = 0
estado_inicial = State(contenedores_iniciales,puerto_inicial,mapa) #estado inicial
nodo_inicial = Node(estado_inicial)
print(nodo_inicial)


lista = [nodo_inicial]

for i in range(3):
    print("\nExpandimos: ")

    n = lista.pop(0) #quita el primero
    n.expandir()
    for child in n.children:
        lista.append(child)
        print(child)


'''
for i in range(20):
    n = a_expandir.pop(0)
    print(n)
    n.expandir()
    for i in n.children:
        a_expandir.append(i)
        print(i)

'''




'''
lista = [nodo_inicial]
contador = 1
while len(lista) > 0:
    print("Iteracion: ", contador)
    n = lista.pop(0)  # coge el primero de la lista
    n.expandir()  # lo expande

    for child in n.children:
        print(child)
        lista.append(child)

    contador += 1

    print("\n")
'''



