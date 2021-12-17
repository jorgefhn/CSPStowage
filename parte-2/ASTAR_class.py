from avl_tree import AVLTree




class AStar():
	def __init__(self,node_inicial,node_final):
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
			n = self.abierta.getMinValueNode(root) #devuelve Nodo
			self.abierta.delete_node(root,n.key) #quita el primer nodo de abierta

			if n.state == self.node_final.state:
				exito = True
				 #verificar si hay que expandir el nodo una vez es el nodo final

			if not exito:
				n.expandir()
				self.cerrada.insert_node(root,n.f,n)

				for child in n.children:
					self.abierta.insert_node(root,child.f,child)

		if exito:
			solucion = n.path
			return solucion

		return("Fracaso")





	
