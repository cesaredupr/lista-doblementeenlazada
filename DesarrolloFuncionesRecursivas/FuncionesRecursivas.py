def convertir_a_binario(numero):
    if numero == 0:
        return ''
    return convertir_a_binario(numero // 2) + str(numero % 2)

def contar_digitos(numero):
    if abs(numero) < 10:
        return 1
    return 1 + contar_digitos(numero // 10)

def calcular_raiz_cuadrada(numero, candidato, minimo, maximo):
    if candidato * candidato == numero:
        return candidato
    if candidato < minimo:
        return calcular_raiz_cuadrada(numero, candidato + 1, minimo, maximo)
    if candidato > maximo:
        return calcular_raiz_cuadrada(numero, candidato - 1, minimo, maximo)
    return calcular_raiz_cuadrada(numero, candidato, minimo, maximo)

def raiz_cuadrada_entera(numero):
    if numero == 0 or numero == 1:
        return numero
    return calcular_raiz_cuadrada(numero, numero // 2, 0, numero)

def convertir_a_decimal(romano):
    romanos = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

    if len(romano) == 0:
        return 0
    if len(romano) == 1:
        return romanos[romano]
    if romanos[romano[0]] < romanos[romano[1]]:
        return romanos[romano[1]] - romanos[romano[0]] + convertir_a_decimal(romano[2:])
    return romanos[romano[0]] + convertir_a_decimal(romano[1:])

def suma_numeros_enteros(numero):
    if numero == 0:
        return 0
    return numero + suma_numeros_enteros(numero - 1)

def mostrar_menu():
    print("Seleccione una opción:")
    print("1. Convertir un número entero a binario")
    print("2. Contar dígitos en un número entero")
    print("3. Calcular raíz cuadrada entera de un número")
    print("4. Convertir un número romano a decimal")
    print("5. Sumar todos los números enteros hasta un número dado")
    print("0. Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("Ingrese el número de la opción deseada: ")

        if opcion == '1':
            numero = int(input("Ingrese un número entero: "))
            print("Representación binaria:", convertir_a_binario(numero))
        elif opcion == '2':
            numero = int(input("Ingrese un número entero: "))
            print("Cantidad de dígitos:", contar_digitos(numero))
        elif opcion == '3':
            numero = int(input("Ingrese un número entero: "))
            print("Raíz cuadrada entera:", raiz_cuadrada_entera(numero))
        elif opcion == '4':
            romano = input("Ingrese un número romano: ")
            print("Equivalente decimal:", convertir_a_decimal(romano))
        elif opcion == '5':
            numero = int(input("Ingrese un número entero: "))
            print("Suma de todos los números enteros:", suma_numeros_enteros(numero))
        elif opcion == '0':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()
