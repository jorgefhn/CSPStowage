def find_deepest_container(mat, num):
  filas = len(mat) 
  columnas = len(mat[0])
  last_row = filas-1
  deepest_one = [None] * columnas

  for fila in range(len(mat)):
    for columna in range(len(mat[0])):
      elem = mat[filas-1-fila][columnas-1-columna]

      if elem == num and deepest_one[columnas-1-columna] is None:
        deepest_one[columnas-1-columna] = [filas-1-fila, columnas-1-columna]
      #print(str(mat[column][last_row]))
    #print()

  #print(deepest_one)
  return deepest_one


def find_greater_above_containers(mat, num, deepest_cord):
  num_of_greater_elems = []
  dic_row_of_greater_elem = {}

  for cord in deepest_cord:
    if cord is not None:
      fila = cord[0]
      columna = cord[1]
      dic_row_of_greater_elem[columna] = []
      cont = 0 

      while fila >= 0:
        if mat[fila][columna] > num and mat[fila][columna] != 0:
          cont +=1
          dic_row_of_greater_elem[columna].append(fila)
        fila -=1
      num_of_greater_elems.append(cont)

    print(num_of_greater_elems)
    print(dic_row_of_greater_elem)

    return num_of_greater_elems, dic_row_of_greater_elem

def h1(mat,num):
    #Heuristica 1: multiplicar por los costes sin tomar en cuenta las posiciones, los elementos que estan mal colocados
    deepest = find_deepest_container(mat,num)
    num_of_greater , dict_pos_of_grater = find_greater_above_containers(mat,num, deepest)
    acum = 0 
    #print_params(deepest, num_of_greater, dict_pos_of_grater)
    for elems in num_of_greater:
      acum += elems * 25

    print("Resultado de la heuristica: " + str(acum)) 
    return acum

def h2(mat,num):
    #Heuristica 2: multiplicar por los costes tomando en cuenta las posiciones, los elementos que estan mal colocados
    deepest = find_deepest_container(mat,num)
    num_of_greater , dict_pos_of_grater = find_greater_above_containers(mat,num, deepest)
    acum = 0 
    #print_params(deepest, num_of_greater, dict_pos_of_grater)
    for column in range(len(deepest)):
      for height in dict_pos_of_grater[column]:
        acum += 25 + 3 * height

    print("Resultado de la heuristica: " + str(acum)) 
    return acum

def h3(mat,num):
    #Heuristica 3: solo tomamos en cuenta los elementos que estan mal colocados
    deepest = find_deepest_container(mat,num)
    num_of_greater , dict_pos_of_grater = find_greater_above_containers(mat,num, deepest)
    acum = 0 
    #print_params(deepest, num_of_greater, dict_pos_of_grater)
    for elems in num_of_greater:
      acum += elems

    print("Resultado de la heuristica: " + str(acum)) 
    return acum

def print_params(deepest, num_of_greater, dict_pos_of_grater):
    print("\n\n\nPosiciones de los unos mas profundos: " + str(deepest))
    print("Numero de elementos mayores que 1 por columna: " + str(num_of_greater))
    print("Diccionarios de las posiciones de los numeros mayores: " + str(dict_pos_of_grater))
