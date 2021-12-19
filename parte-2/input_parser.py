
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

