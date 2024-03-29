
def find_deepest_container(mat, num):
  """método para devolver el contenedor ´con puerto = num más profundo"""
  filas,columnas = len(mat),len(mat[0])
  deepest_one = [None] * columnas

  for fila in range(filas):
    for columna in range(columnas):
      elem = mat[filas-1-fila][columnas-1-columna]

      if elem == num and deepest_one[columnas-1-columna] is None: #ha encontrado el más profundo
        deepest_one[columnas-1-columna] = [filas-1-fila, columnas-1-columna]

  return deepest_one


def find_greater_above_containers(mat, num, deepest_cord):
  """busca la cantidad de elementos > num y las posiciones de dichos elementos"""

  num_of_greater_elems, dic_row_of_greater_elem = [],{}

  for cord in deepest_cord:

    if cord is not None:

      fila,columna,dic_row_of_greater_elem[columna],cont = cord[0],cord[1],[],0

      while fila >= 0:
        if mat[fila][columna] > num and mat[fila][columna] != -1:
          cont +=1
          dic_row_of_greater_elem[columna].append(fila)

        fila -=1
      
      num_of_greater_elems.append(cont)


    return num_of_greater_elems, dic_row_of_greater_elem




########## IMPLEMENTACIÓN DE LAS HEURÍSTICAS ###############

def h1(mat,num):
    #Heuristica 1: multiplicar por los costes sin tomar en cuenta las posiciones, los elementos que estan mal colocados
    deepest = find_deepest_container(mat,num)
    num_of_greater , dict_pos_of_grater = find_greater_above_containers(mat,num, deepest)
    acum = 0 
    for elems in num_of_greater:
      acum += elems * 25

    return acum


def h2(mat, num):
    #Heuristica 2: multiplicar por los costes tomando en cuenta las posiciones, los elementos que estan mal colocados
    deepest = find_deepest_container(mat,num)
    num_of_greater , dict_pos_of_grater = find_greater_above_containers(mat,num, deepest)
    acum = 0
    for column in dict_pos_of_grater:
      for height in dict_pos_of_grater[column]:
          acum += 25 + 3 * height
    return acum


def h3(mat,num):
    #Heuristica 3: solo tomamos en cuenta los elementos que estan mal colocados
    deepest = find_deepest_container(mat,num)
    num_of_greater , dict_pos_of_grater = find_greater_above_containers(mat,num, deepest)
    acum = 0 
    for elems in num_of_greater:
      acum += elems

    return acum




def h4(mat,num,puerto_final):
    #Heuristica 4: Heuristica 1 + informada desde el inicial. No es admisible (no siempre consigue la solución óptima)
    deepest = find_deepest_container(mat,num)
    num_of_greater , dict_pos_of_grater = find_greater_above_containers(mat,num, deepest)
    acum = 0 
    for elems in num_of_greater:
      acum += elems * 25

    cant_navv = puerto_final - num
    acum += cant_navv*3500

    return acum
