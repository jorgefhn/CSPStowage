# --------------------------------------------------------
#.out
def output_sol(mapa,contenedores,heuristica, ult_nodo):
    """función auxiliar para devolver fichero .output"""

    file = open(mapa + "-" + contenedores + "-" + heuristica + ".output", "w")
    file.write("ID de accion"+"\t|\t"+" Accion"+"\t\t|\t"+"Contenedor / Origen"+"\t|\t"+" Posicion / Destino"+"\t|\n")

    if ult_nodo != -1: #ha encontrado solución

        for i in range(len(ult_nodo.actions)): 
            accion = ult_nodo.actions[i][0]

            if accion == "Cargar":
                id = ult_nodo.actions[i][1]
                posicion = str(ult_nodo.actions[i][2]) + "," + str(ult_nodo.actions[i][3])
                file.write("\t" + str(i) + ".\t\t\t|\t" + accion + "\t\t|\t\t\t" + id + "\t\t\t|\t\t\t" + posicion +"\t\t\t|\n")

            elif accion == "Descargar":
                id = ult_nodo.actions[i][1]
                posicion = str(ult_nodo.actions[i][2]) + "," + str(ult_nodo.actions[i][3])
                file.write("\t" + str(i) + ".\t\t\t|\t" + accion + "\t|\t\t\t" + id + "\t\t\t|\t\t\t" + posicion + "\t\t\t|\n")
            
            else: #navegar
                origen = str(ult_nodo.actions[i][1])
                destino = str(ult_nodo.actions[i][2])
                file.write("\t" + str(i) + ".\t\t\t|\t" + accion + "\t\t|\t\t\t" + origen + "\t\t\t|\t\t\t " + destino +"\t\t\t|\n")
    file.close()


# .stat
def stat_sol(mapa, contenedores,heuristica, t_inicio, t_final, ult_nodo, nodos_expandidos):
    """Función auxiliar para devolver fichero .stat"""
    file = open(mapa + "-" + contenedores + "-" + heuristica + ".stat", "w")
    file.write("Tiempo total: " + str(t_final - t_inicio))

    if ult_nodo != -1: #ha encontrado solución
        file.write("\nCoste total: " + str(ult_nodo.costeTotal()))
        file.write("\nLongitud del plan: " + str(len(ult_nodo.actions)))

    file.write("\nNodos expandidos: " + str(nodos_expandidos))

    file.close()

