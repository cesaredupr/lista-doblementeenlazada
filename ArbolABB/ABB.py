import graphviz

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert_recursive(self.root, key)

    def _insert_recursive(self, root, key):
        if root is None:
            return TreeNode(key)
        if key < root.key:
            root.left = self._insert_recursive(root.left, key)
        elif key > root.key:
            root.right = self._insert_recursive(root.right, key)
        return root

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, root, key):
        if root is None or root.key == key:
            return root
        if key < root.key:
            return self._search_recursive(root.left, key)
        return self._search_recursive(root.right, key)

    def delete(self, key):
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, root, key):
        if root is None:
            return root
        if key < root.key:
            root.left = self._delete_recursive(root.left, key)
        elif key > root.key:
            root.right = self._delete_recursive(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            temp = self._min_value_node(root.right)
            root.key = temp.key
            root.right = self._delete_recursive(root.right, temp.key)
        return root

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def load_from_file(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                key = int(line.strip())
                self.insert(key)

    def visualize(self):
        dot = graphviz.Digraph()
        self._visualize_recursive(self.root, dot)
        dot.render('binary_search_tree', format='png', cleanup=True)
        dot.view()

    def _visualize_recursive(self, root, dot):
        if root:
            dot.node(str(root.key))
            if root.left:
                dot.edge(str(root.key), str(root.left.key))
                self._visualize_recursive(root.left, dot)
            if root.right:
                dot.edge(str(root.key), str(root.right.key))
                self._visualize_recursive(root.right, dot)

def print_menu():
    print("\nMenu:")
    print("1. Insertar nodo")
    print("2. Buscar nodo")
    print("3. Eliminar nodo")
    print("4. Cargar datos desde archivo")
    print("5. Visualizar árbol")
    print("6. Salir")

if __name__ == "__main__":
    bst = BinarySearchTree()
    while True:
        print_menu()
        choice = input("Ingrese su elección: ")
        if choice == '1':
            key = int(input("Ingrese el valor del nodo a insertar: "))
            bst.insert(key)
        elif choice == '2':
            key = int(input("Ingrese el valor del nodo a buscar: "))
            node = bst.search(key)
            if node:
                print(f"El nodo con el valor {key} está presente en el árbol.")
            else:
                print(f"El nodo con el valor {key} no está presente en el árbol.")
        elif choice == '3':
            key = int(input("Ingrese el valor del nodo a eliminar: "))
            bst.delete(key)
        elif choice == '4':
            file_path = input("Ingrese la ruta del archivo de datos: ")
            bst.load_from_file(file_path)
        elif choice == '5':
            bst.visualize()
        elif choice == '6':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, ingrese una opción válida.")

