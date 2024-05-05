import numpy as np
from graphviz import Digraph
import matplotlib.pyplot as plt

class matrizDispersa:
    def __init__(self):
        self.main_matrix = []
       
    def cargar_csv_a_matriz(self,archivo):        
        for linea in archivo:
            self.main_matrix.append(linea)
            
    def mostrar_matriz(self):
        for linea in self.main_matrix:
            #for ele in linea:
                #print(linea[ele])
            print(linea)

    def insertar_matriz(self):
        n_row = int(input("Ingrese el numero de filas que desea insertar en la matriz: "))
        n_col = int(input("Ingrese el numero de columnas que desea insertar en la matriz: "))
        for i in range(n_row):
            insert_matriz_manual = []
            print(f"---- Ingrese los datos de la FILA  {i+1} ----")
            for j in range(n_col):
                indice = int(input("Ingrese el valor de las columna: "))
                insert_matriz_manual.append(indice)
            #print(insert_matriz_manual)
            self.main_matrix.append(insert_matriz_manual)
            #print(self.main_matrix)
    
    def generar_grafica(self):
        matrix = self.main_matrix
           # Crear un gráfico dirigido
        dot = Digraph()

        # Obtener dimensiones de la matriz
        rows, cols = matrix.shape

        # Crear nodos para cada celda de la matriz
        for i in range(rows):
            for j in range(cols):
                # Agregar nodos con etiquetas de fila y columna
                dot.node(f'{i}_{j}', label=str(matrix[i][j]))

                # Agregar nodos adicionales para unir las celdas
                if i < rows - 1:
                    dot.node(f'{i+1}_{j}', label='', style='invisible')
                    dot.edge(f'{i}_{j}', f'{i+1}_{j}', style='invisible')
                if j < cols - 1:
                    dot.node(f'{i}_{j+1}', label='', style='invisible')
                    dot.edge(f'{i}_{j}', f'{i}_{j+1}', style='invisible')

        # Dibujar el gráfico
        dot.attr(rankdir='LR')
        dot.attr(splines='line')
        dot.attr(dpi='300')
        dot.attr(label=f'Matrix\n{matrix}', fontsize='12')
        dot.attr(fontsize='10')
        dot.format = 'png'
        dot.render('matrix_graph', cleanup=True)

        # Mostrar la imagen generada
        img = plt.imread('matrix_graph.png')
        plt.imshow(img)
        plt.axis('off')
        plt.show()

   

try:
    if __name__ == "__main__":
        opc = 0
        nMatriz = matrizDispersa()

        while opc != 6:
            print("\n------------------------------------------------",)
            print("**** Menu de Matriz Dispersa ****", end='\n')
            print("Elige una opción (Número) para ingresar hacer una acción")
            print("-------------------------------------------------")
            print("1 - Cargar el archivo CSV para la matriz dispersa")
            print("2 - Ingresar la matriz dispersa manualmente")
            print("3 - Visualizar los datos de la matriz por consola")
            print("4 - Generar gráfica de la matriz")
            print("5 - Salir")
            opc = int(input("Ingrese su opción(Número): "))

            if opc == 1:
                nombre_archivo = input("Arrastra el archivo CSV para la matriz dispersa: ")
                with open(nombre_archivo, "r") as archivo:
                    #matrix.append([linea])
                    nMatriz.cargar_csv_a_matriz(archivo)
            elif opc == 2:
                nMatriz.insertar_matriz()
            elif opc == 3:
                nMatriz.mostrar_matriz()
            elif opc == 4:
                nMatriz.generar_grafica()
            elif opc == 5:
                  print("Sesión Terminada, si necesita ingresar nuevamente ejecute el codigo en CLI")
            else:
                print("opción inválida.")
except Exception as e:
    print(e)

#------------------------------------------------------------------------------#
#matrix = np.array([[1, 2, 3],[4, 5, 6],[7, 8, 9]])
#nmatrix = np.array(nMatriz.main_matrix)

