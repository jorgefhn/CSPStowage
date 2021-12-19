# versión que estamos probando


from argparse import ArgumentParser
from heuristicas import h1, h2, h3

from queue import PriorityQueue
import copy
import time
import sys
from heapdict import heapdict
import outputs_sol
import input_parser

"""################### OBTENCION DE LOS FICHEROS DESDE STDIN #######################"""

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


# --------------------------------------------------------

# mapa, contenedores, matriz con el mapa
mapa = open(ruta_mapa).read()
contenedores = open(ruta_contenedores).read()
array_contenedores = input_parser.devuelveContenedores(contenedores)
mapa = input_parser.generateMap(mapa)
n_pilas, max_prof = len(mapa[0]), len(mapa)

print("Contenedores:")
print(array_contenedores)
print("Generamos mapa: ")
print(input_parser.drawMap(mapa))


"""########################## CODIGO RELATIVO A LA IMPLEMENTACION ##################################"""


class State:
    def __init__(self, contenedores: list, puerto_actual_del_barco: int, mapa: list):
        self.contenedores = contenedores
        self.puerto_del_barco = puerto_actual_del_barco
        self.mapa = mapa
        self.asignados = {}

    def __str__(self):
        var = str(self.contenedores) + "\n"
        var += str(input_parser.drawMap(self.mapa)) + "\n"
        var += str(self.asignados)
        var += "\nPuerto del barco: " + str(self.puerto_del_barco) + "\n"
        return var

    def __eq__(self, other):
        return self.contenedores == other.contenedores and self.mapa == other.mapa and self.puerto_del_barco == other.puerto_del_barco and self.asignados == other.asignados


class Node:

    def __init__(self, state, parent=None, g=0, h=0, actions=[], id_heuristica=args.heuristica):
        self.children = []      # lista de nodos hijos
        self.parent = parent    # si tiene nodo padre o no
        self.g = g              # funcion de costes de operadores aplicados
        self.state = state
        self.h = self.elegirHeuristica(id_heuristica)
        self.f = self.costeTotal()  # distancia del nodo al nodo inicial (ver si se puede usar)

        if parent:
            self.path = parent.path
            self.actions = parent.actions
        else:
            self.path = []
            self.actions = []

    # métodos propios del nodo
    def __str__(self):
        var = str(self.state) + "\nFunción de evaluación: " + str(self.costeTotal()) + "\n"
        return var

    def checkEqual(self, other):
        return self.state == other.state

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
            self.state.mapa[x][y] = self.devolver_tipo(posicion)  # devolvemos a la casilla que había

            self.state.contenedores[posicion] = [None, None, self.state.puerto_del_barco]  # desasigna su posición
            self.state.asignados.pop(id)  # borra el elemento de la lista de asignados
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
        x, y = self.state.contenedores[posicion][0], self.state.contenedores[posicion][1]
        return str(mapa[x][y])

    def contenedor_compatible(self, posicion, x, y):
        contenedor = array_contenedores[posicion]

        if (contenedor[1] == "R" and self.state.mapa[x][y] == "E") or (
                contenedor[1] == "S" and self.state.mapa[x][y] in ("E", "N")):
            return True

        return False

    def elegirHeuristica(self, id_heuristica: str):
        """método de elegir heurística"""

        mapa = self.retornaPuertos()

        if id_heuristica == "h1":
            return h1(mapa, self.state.puerto_del_barco)

        if id_heuristica == "h2":
            return h2(mapa,self.state.puerto_del_barco)

        if id_heuristica == "h3":
            return h3(mapa, self.state.puerto_del_barco)

    # metodo que crea nodos
    def generateNode(self, new_contenedores: list, coste: int, new_asignados: list, new_mapa: list, new_puerto):
        """método auxiliar que genera nodo"""
        new_state = State(new_contenedores, new_puerto, new_mapa)
        new_state.asignados = new_asignados

        new_node = Node(new_state, self)
        new_node.g += coste
        return new_node

    #metodo que calcula la f del nodo
    def costeTotal(self):
        return self.g + self.h

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

    def checkDifferent(self, new_node, new_contenedores: list, cont: int, action: str, cont_id=None, pos_x = None, pos_y = None):

        if new_contenedores[cont] != self.state.contenedores[cont] and new_node not in self.path:

            self.children.append(new_node)  # añade el nodo a los hijos
            new_node.path.append(self)

            new_actions = copy.deepcopy(self.actions)

            if action == "carga":
                # id del contenedor,posición x,y y puerto
                ac = ["Cargar", array_contenedores[cont][0], new_contenedores[cont][0],
                      new_contenedores[cont][1], self.state.puerto_del_barco]
                new_actions.append(ac)

            new_node.actions = new_actions

    #metodo que expande un nodo
    def expandir(self):

        # crear todas las posibilidades válidas y añadirlas
        posibles_coordenadas = self.generateCoordinates()  # genera las posibles coordenadas

        if self.checkNavigate():
            new_node = self.generateNode(self.state.contenedores, self.g + 3500, self.state.asignados, self.state.mapa,
                                         self.state.puerto_del_barco + 1)  # generamos nuevo nodo


            ac = ["Navegar", self.state.puerto_del_barco, self.state.puerto_del_barco + 1]
            new_node.actions.append(ac)
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
                pos_x = copy.deepcopy(x)
                pos_y = copy.deepcopy(y)
                cont_nuevo = new_node.checkReordenate(cont, pos_x, pos_y)


                new_node.descargar(cont_nuevo)

                self.checkDifferent(new_node, new_contenedores, cont_nuevo, action, array_contenedores[cont][0],pos_x,pos_y)

                ac = ["Descargar", array_contenedores[cont_nuevo][0], x_antes, y_antes, self.state.puerto_del_barco]
                new_node.actions.append(ac)


            elif action == "carga":

                for pos in posibles_coordenadas:  # por cada posible combinación
                    x, y = pos[0], pos[1]
                    new_contenedores = copy.deepcopy(
                        self.state.contenedores)  # creamos nueva lista de contenedores para el nuevo estado
                    coste, contenedor, new_mapa, new_asignados = self.generateParams(cont)[1:]

                    new_node = self.generateNode(new_contenedores, coste, new_asignados, new_mapa,
                                                 self.state.puerto_del_barco)  # generamos un nuevo nodo


                    new_node.cargar(cont, x, y)
                    self.checkDifferent(new_node, new_contenedores, cont, action)


def busqueda(nodo_inicial, nodo_final):
    """método de búsqueda de A*"""
    result = [-1, -1]
    nodos_expandidos = 0
    abierta = heapdict()
    cerrada = heapdict()
    exito = False
    abierta[nodo_inicial] = nodo_inicial.f
    #print(nodo_inicial.f)
    while len(abierta.keys()) > 0 and not exito:

        minimo = abierta.peekitem()[0]

        #print("Minimo que vamos a comprobar: ", minimo)

        #print("Mínimo en cerrada: ", cerrada.get(minimo))

        if cerrada.get(minimo) is None:

            minimo = abierta.popitem()[0]  # quita el primer nodo de abierta

            if minimo.checkEqual(nodo_final):
                exito = True

        if not exito:
            minimo.expandir()
            nodos_expandidos += 1
            cerrada[minimo] = minimo.f

            #print("Cerrada: ", list(cerrada.keys()))

            for child in minimo.children:
                abierta[child] = child.f

    if exito:
        print("Solución encontrada")
        result[0]=minimo
        result[1]=nodos_expandidos
        return result


    else:
        print("Fracaso")
        return result



# --------------------------------------------------------

# obtenemos el puerto final
puerto_final = 0
for cont in array_contenedores:
    if int(cont[2]) > puerto_final:
        puerto_final = int(cont[2])

contenedores_iniciales = []
contenedores_finales = []
for cont in array_contenedores:
    contenedores_iniciales.append([None, None, 0])
    contenedores_finales.append([None, None, int(cont[2])])

"""################################# SIMULACION DEL MAIN #############################################"""

puerto_inicial = 0
estado_inicial = State(contenedores_iniciales, puerto_inicial, mapa)  # estado inicial
estado_final = State(contenedores_finales, puerto_final, mapa)

nodo_inicial = Node(estado_inicial)
nodo_final = Node(estado_final)

t_inicio = time.time()
ult_nodo, nodos_expandidos = busqueda(nodo_inicial, nodo_final)
t_final = time.time()

# ----------------------------------------- Save Output ---------------------------------------------------
outputs_sol.output_sol(args.mapa,args.contenedores,args.heuristica, ult_nodo)
outputs_sol.stat_sol(args.mapa, args.contenedores, args.heuristica, t_inicio, t_final, ult_nodo, nodos_expandidos)





