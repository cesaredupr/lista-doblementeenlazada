import csv

# Nodo de una lista enlazada
class Node:
    def __init__(self, key, value):
        self.key = key       # Clave del nodo
        self.value = value   # Valor del nodo
        self.next = None     # Referencia al siguiente nodo (para encadenamiento)

# Tabla hash con encadenamiento
class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [None] * size  # Arreglo de tamaño fijo

    def _hash_function(self, key):
        return hash(key) % self.size  # Calcula el índice usando la función hash y el operador módulo

    def insert(self, key, value):
        index = self._hash_function(key)
        new_node = Node(key, value)
        
        if self.table[index] is None:
            self.table[index] = new_node  # Inserta el nodo si la posición está vacía
        else:
            current = self.table[index]
            while current.next is not None:
                if current.key == key:
                    current.value = value  # Actualiza el valor si la clave ya existe
                    return
                current = current.next
            if current.key == key:
                current.value = value  # Actualiza el valor si la clave ya existe
            else:
                current.next = new_node  # Añade el nuevo nodo al final de la lista enlazada

    def get_by_key(self, key):
        index = self._hash_function(key)
        current = self.table[index]
        while current is not None:
            if current.key == key:
                return current.value  # Devuelve el valor si encuentra la clave
            current = current.next
        return None  # Devuelve None si no encuentra la clave

    def get_by_value(self, value):
        for i in range(self.size):
            current = self.table[i]
            while current is not None:
                if current.value == value:
                    return current.key  # Devuelve la clave si encuentra el valor
                current = current.next
        return None  # Devuelve None si no encuentra el valor

    def display(self):
        for i in range(self.size):
            current = self.table[i]
            if current:
                print(f"Index {i}: ", end="")
                while current:
                    print(f"({current.key}: {current.value})", end=" -> ")
                    current = current.next
                print("None")

    def load_from_csv(self, file_path):
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 2:
                    key, value = row
                    self.insert(key, value)

# Función principal para la interacción con el usuario
def main():
    hash_table = HashTable()

    while True:
        print("\n1. Insertar dato")
        print("2. Buscar por clave")
        print("3. Buscar por valor")
        print("4. Mostrar tabla")
        print("5. Cargar datos desde CSV")
        print("6. Salir")

        choice = input("Seleccione una opción: ")

        if choice == '1':
            key = input("Ingrese la clave: ")
            value = input("Ingrese el valor: ")
            hash_table.insert(key, value)
            print(f"Dato insertado: ({key}: {value})")

        elif choice == '2':
            key = input("Ingrese la clave a buscar: ")
            value = hash_table.get_by_key(key)
            if value:
                print(f"Valor encontrado para la clave '{key}': {value}")
            else:
                print(f"Clave '{key}' no encontrada")

        elif choice == '3':
            value = input("Ingrese el valor a buscar: ")
            key = hash_table.get_by_value(value)
            if key:
                print(f"Clave encontrada para el valor '{value}': {key}")
            else:
                print(f"Valor '{value}' no encontrado")

        elif choice == '4':
            hash_table.display()

        elif choice == '5':
            file_path = input("Ingrese la ruta del archivo CSV: ")
            hash_table.load_from_csv(file_path)
            print("Datos cargados desde el archivo CSV")

        elif choice == '6':
            break

        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()

