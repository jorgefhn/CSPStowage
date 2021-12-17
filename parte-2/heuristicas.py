mat = [ [2,2,1,1],
        [2,1,2,1],
        [1,2,1,2],
        [1,1,2,2]
      ]

mat2= [ [2],
        [2],
        [1],
        [1]
      ]

#print("Esta es la cantidad de fila: ", len(mat2))
#print("Esta es la cantidad de comlunas: ", len(mat2[0]))

def find_deepest_container(mat, num):
  filas = len(mat) 
  columnas = len(mat[0])
  last_row = filas-1
  deepest_one = [None] * columnas

  while last_row > 0:
    for column in range(columnas):
      elem = mat[column][last_row]
      if elem == num and deepest_one[column] is None:
        deepest_one[column] = [last_row, column]
      #print(str(mat[column][last_row]))
    last_row-=1
    #print()

  #print(deepest_one)
  return deepest_one

def find_greater_above_containers(mat, num, deepest_cord):
  num_of_greater_elems = []
  dic_row_of_greater_elem = {}

  for cord in deepest_cord:
    fila = cord[0]
    columna = cord[1]
    dic_row_of_greater_elem[columna] = []
    cont = 0 

    while fila >= 0:
      if mat[fila][columna] > num:
        cont +=1
        dic_row_of_greater_elem[columna].append(fila)
      fila -=1
    num_of_greater_elems.append(cont)

  return num_of_greater_elems, dic_row_of_greater_elem




def h1(mat,num):
    deepest = find_deepest_container(mat,num)
    num_of_greater , dict_pos_of_grater = find_greater_above_containers(mat,num, deepest)
    print("\n\n\nPosiciones de los unos mas profundos: " + str(deepest))
    print("Numero de elementos mayores que 1 por columna: " + str(num_of_greater))
    print("Diccionarios de las posiciones de los numeros mayores: " + str(dict_pos_of_grater))

    #Heuristica 1: multiplicar por los costes sin tomar en cuenta las posiciones, los elementos que estan mal colocados
    acum = 0 
    for elems in num_of_greater:
      acum += elems * 25

    print("Resultado de la heuristica: " + str(acum)) 

h1(mat,1)

def h2(mat,num):
    deepest = find_deepest_container(mat,num)
    num_of_greater , dict_pos_of_grater = find_greater_above_containers(mat,num, deepest)
    print("\n\n\nPosiciones de los unos mas profundos: " + str(deepest))
    print("Numero de elementos mayores que 1 por columna: " + str(num_of_greater))
    print("Diccionarios de las posiciones de los numeros mayores: " + str(dict_pos_of_grater))

    #Heuristica 1: multiplicar por los costes sin tomar en cuenta las posiciones, los elementos que estan mal colocados
    acum = 0 
    for elems in num_of_greater:
      acum += elems * 25

    print("Resultado de la heuristica: " + str(acum)) 

h2(mat,1)

def h3(mat,num):
    deepest = find_deepest_container(mat,num)
    num_of_greater , dict_pos_of_grater = find_greater_above_containers(mat,num, deepest)
    print("\n\n\nPosiciones de los unos mas profundos: " + str(deepest))
    print("Numero de elementos mayores que 1 por columna: " + str(num_of_greater))
    print("Diccionarios de las posiciones de los numeros mayores: " + str(dict_pos_of_grater))

    #Heuristica 1: multiplicar por los costes sin tomar en cuenta las posiciones, los elementos que estan mal colocados
    acum = 0 
    for elems in num_of_greater:
      acum += elems * 25

    print("Resultado de la heuristica: " + str(acum)) 

h3(mat,1)
