from graphviz import Digraph

class Nodo:
    def __init__(self, nombre, apellido, carnet):
        self.nombre = nombre
        self.apellido = apellido
        self.carnet = carnet
        self.siguiente = None
        self.anterior = None

class ListaDoblementeEnlazada:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0

    def vacia(self):
        return self.primero == None    

    def agregar_final(self, nombre, apellido, carnet):
        if self.vacia():
            self.primero = self.ultimo = Nodo(nombre, apellido, carnet)
        else:
            aux = self.ultimo
            self.ultimo = aux.siguiente = Nodo(nombre, apellido, carnet)
            self.ultimo.anterior = aux
        self.size += 1

    def agregar_inicio(self, nombre, apellido, carnet):
        if self.vacia():
            self.primero = self.ultimo = Nodo(nombre, apellido, carnet)
        else:
            aux = Nodo(nombre, apellido, carnet)
            aux.siguiente = self.primero
            self.primero.anterior = aux
            self.primero = aux
        self.size += 1

    def recorrer_inicio(self): 
        aux = self.primero
        while aux != None:
            print(f"Nombre: {aux.nombre}, Apellido: {aux.apellido}, Carnet: {aux.carnet}", end=" ")
            aux = aux.siguiente

    def recorrer_final(self): 
        aux = self.ultimo
        while aux:
            print(f"Nombre: {aux.nombre}, Apellido: {aux.apellido}, Carnet: {aux.carnet}", end=" ")
            aux = aux.anterior

    def eliminar_inicio(self): 
        if self.vacia():
            print("Lista vacía")
        elif self.primero.siguiente == None:
            self.primero = self.ultimo = None
            self.size = 0
        else:
            self.primero = self.primero.siguiente
            self.primero.anterior = None
            self.size -= 1

    def eliminar_final(self):
        if self.vacia():
            print("Lista vacía")
        elif self.primero.siguiente == None:
            self.primero = self.ultimo = None
            self.size = 0
        else:
            self.ultimo = self.ultimo.anterior
            self.ultimo.siguiente = None
            self.size -= 1

    def generar_grafica(self):
        dot = Digraph(comment='Lista Doblemente Enlazada')
        dot.node_attr['shape'] = 'record'
        dot.graph_attr['rankdir'] = 'LR'
        dot.edge_attr.update(arrowhead='vee', arrowsize='0.7')

        nodo_actual = self.primero
        while nodo_actual:
            label = f'{{<prev> | {{<data> Nombre: {nodo_actual.nombre} | Apellido: {nodo_actual.apellido} | Carnet: {nodo_actual.carnet} }} | <next>}}'
            dot.node(str(id(nodo_actual)), label=label)
            if nodo_actual.siguiente:
                dot.edge(str(id(nodo_actual)), str(id(nodo_actual.siguiente)), label='Siguiente')
            if nodo_actual.anterior:
                dot.edge(str(id(nodo_actual)), str(id(nodo_actual.anterior)), label='Anterior')
            nodo_actual = nodo_actual.siguiente

        return dot

try:
    if __name__ == "__main__":
        opcion = 0
        lista = ListaDoblementeEnlazada()
        while opcion != 8:
            print("\n--- Lista Doblemente Enlazada ---\n 1. Agregar nodo al final\n 2. Eliminar nodo al final\n 3. Agregar nodo al inicio\n 4. Eliminar nodo al inicio\n 5. Mostrar en orden ascendente\n 6. Mostrar en orden descendente\n 7. Mostrar gráfica\n 8. Salir")
            opcion = int(input("Ingrese su opción: "))

            if opcion == 1:
                nombre = input("Ingresa el nombre: ")
                apellido = input("Ingresa el apellido: ")
                carnet = input("Ingresa el carnet: ")
                lista.agregar_final(nombre, apellido, carnet)
            elif opcion == 2:
                lista.eliminar_final()
            elif opcion == 3:
                nombre = input("Ingresa el nombre: ")
                apellido = input("Ingresa el apellido: ")
                carnet = input("Ingresa el carnet: ")
                lista.agregar_inicio(nombre, apellido, carnet)
            elif opcion == 4:
                lista.eliminar_inicio()
            elif opcion == 5:
                lista.recorrer_inicio()
            elif opcion == 6:
                lista.recorrer_final()
            elif opcion == 7:
                graph = lista.generar_grafica()
                graph.render('lista_doblemente_enlazada', format='png', view=True)
            elif opcion == 8:
                print("Sesión culminada")
            else:
                print("Ingresaste una opción errónea, vuelve a intentarlo.")
except Exception as e:
    print(e)
