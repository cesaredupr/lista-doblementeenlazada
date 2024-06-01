import pygame 
import sys
import random 
import pickle
import numpy as np
import graphviz
import subprocess

class Nodo:
    def __init__(self, dato): #Constructor 
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, dato):
        if not self.cabeza:
            self.cabeza = Nodo(dato)
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = Nodo(dato)

    def obtener(self, indice):
        actual = self.cabeza
        for _ in range(indice):
            if actual:
                actual = actual.siguiente
            else:
                return None
        return actual.dato if actual else None

    def actualizar(self, indice, dato):
        actual = self.cabeza
        for _ in range(indice):
            if actual:
                actual = actual.siguiente
            else:
                return
        if actual:
            actual.dato = dato

    def a_lista(self): #De ListaEnlazada a ListaPython 
        lista = []
        actual = self.cabeza
        while actual:
            lista.append(actual.dato)
            actual = actual.siguiente
        return lista

    def generar_grafico(self, nombre_archivo):
        dot = graphviz.Digraph()
        dot.attr(rankdir='LR')  # Direccion horizontal
        actual = self.cabeza
        indice = 0
        while actual:
            dot.node(f'nodo{indice}', actual.dato)
            if actual.siguiente:
                dot.edge(f'nodo{indice}', f'nodo{indice + 1}')
            actual = actual.siguiente
            indice += 1
        dot.render(nombre_archivo, format='png', cleanup=True)

class JuegoTikTakToe:
    def __init__(self):
        self.tablero = ListaEnlazada()
        for _ in range(9):
            self.tablero.agregar('-')
        self.jugador = 'X'
        self.movimientos_x = 0  # Contador de movimientos de X
        self.historial = []
        self.q_table = self.cargar_q_table()
        self.alpha = 0.1  # Tasa de aprendizaje
        self.gamma = 0.9  # Factor de descuento

    def reiniciar_tablero(self):
        self.tablero = ListaEnlazada()
        for _ in range(9):
            self.tablero.agregar('-')
        self.jugador = 'X'
        self.movimientos_x = 0  # Reiniciar el contador de movimientos

    def realizar_movimiento(self, posicion): #Valida movimiento del usuario "X"
        if self.tablero.obtener(posicion) == '-':
            self.tablero.actualizar(posicion, self.jugador)
            if self.jugador == 'X':
                self.movimientos_x += 1  # Incrementar el contador de movimientos de X
            if self.verificar_ganador():
                ponderacion = self.calcular_ponderacion_x()
                self.historial.append(f'{self.jugador} gana con ponderación {ponderacion}')
                self.actualizar_q_table(1 if self.jugador == 'O' else -1)
                self.tablero.generar_grafico('tablero')
                return True
            elif '-' not in self.tablero.a_lista():
                self.historial.append('Empate')
                self.actualizar_q_table(0.5)
                self.tablero.generar_grafico('tablero')
                return True
            else:
                self.jugador = 'O' if self.jugador == 'X' else 'X'
                return False
        return False

    def calcular_ponderacion_x(self): #Realiza el calculo de la ponderacion
        max_movimientos = 9
        ponderacion = max_movimientos - self.movimientos_x + 1
        return ponderacion

    def abrir_grafico(self, archivo):
        if sys.platform == "win32":
            subprocess.run(['start', archivo], shell=True)
        elif sys.platform == "darwin":
            subprocess.run(['open', archivo])
        else:
            subprocess.run(['xdg-open', archivo])

    def cargar_q_table(self):
        try:
            with open('q_table.pkl', 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def guardar_q_table(self):
        with open('q_table.pkl', 'wb') as f:
            pickle.dump(self.q_table, f)

    def actualizar_q_table(self, recompensa):
        estado = ''.join(self.tablero.a_lista())
        if estado not in self.q_table:
            self.q_table[estado] = np.zeros(9)
        max_q_nuevo_estado = max(self.q_table[estado]) if estado in self.q_table else 0
        for i in range(9):
            if self.tablero.obtener(i) == '-':
                self.q_table[estado][i] += self.alpha * (recompensa + self.gamma * max_q_nuevo_estado - self.q_table[estado][i])

    def movimiento_bot(self): #Valida movimientos del bot
        estado = ''.join(self.tablero.a_lista())
        if estado not in self.q_table:
            self.q_table[estado] = np.zeros(9)
        movimientos_posibles = [i for i in range(9) if self.tablero.obtener(i) == '-']
        if random.random() < 0.2:
            movimiento = random.choice(movimientos_posibles) 
        else:
            max_recompensa = max(self.q_table[estado][i] for i in movimientos_posibles)
            mejores_movimientos = [i for i in movimientos_posibles if self.q_table[estado][i] == max_recompensa]
            movimiento = random.choice(mejores_movimientos)
        self.realizar_movimiento(movimiento)   

    def verificar_ganador(self): #Este bloque se ejecuta despues de cada movimiento en el tablero
        combinaciones_ganadoras = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        tablero_lista = self.tablero.a_lista()
        for combinacion in combinaciones_ganadoras:
            if tablero_lista[combinacion[0]] == tablero_lista[combinacion[1]] == tablero_lista[combinacion[2]] != '-':
                return True
        return False

class InterfazTikTakToe:
    def __init__(self, juego):
        self.juego = juego
        pygame.init() 
        self.tamaño_ventana = 600
        self.ventana = pygame.display.set_mode((self.tamaño_ventana, self.tamaño_ventana))
        pygame.display.set_caption('Tik Tak Toe')
        self.fuente = pygame.font.Font(None, 200)  # Tamaño de la fuente ajustado
        self.menu_activo = True
        self.juego_terminado = False

    def mostrar_menu(self):
        self.ventana.fill((255, 255, 255))
        opciones = ["1. Jugar", "2. Ver Historial", "3. Ver Desarrollador", "4. Salir"]
        self.opciones_rects = []
        for i, opcion in enumerate(opciones):
            texto = pygame.font.Font(None, 36).render(opcion, True, (0, 0, 0))
            rect = texto.get_rect(topleft=(100, 150 + i * 50))
            self.opciones_rects.append((rect, opcion))
            self.ventana.blit(texto, rect.topleft)
        pygame.display.flip()

    def mostrar_historial(self): #Historial de partidas
        self.ventana.fill((255, 255, 255))
        historial = self.juego.historial
        for i, resultado in enumerate(historial):
            texto = pygame.font.Font(None, 36).render(f'Partida {i + 1}: {resultado}', True, (0, 0, 0))
            self.ventana.blit(texto, (10, 10 + i * 30))
        pygame.display.flip()
        self.esperar_tecla()

    def mostrar_desarrolladores(self):
        self.ventana.fill((255, 255, 255))
        desarrollador = "Desarrollador: César Eduardo Paredes Ramos"
        carnet = "Carnet: 9490-17-893"
        seccion_c = "Sección: C"
        texto_desarrollador = pygame.font.Font(None, 36).render(desarrollador, True, (0, 0, 0))
        texto_carnet = pygame.font.Font(None, 36).render(carnet, True, (0, 0, 0))
        texto_seccion_c = pygame.font.Font(None, 36).render(seccion_c, True, (0, 0, 0))
        self.ventana.blit(texto_desarrollador, (10, 10))
        self.ventana.blit(texto_carnet, (10, 50))
        self.ventana.blit(texto_seccion_c, (10, 90))
        pygame.display.flip()
        self.esperar_tecla()

    def mostrar_ganador(self, ganador):
        self.ventana.fill((0, 0, 0))  # Fondo negro
        if ganador == 'Empate':
            mensaje = '¡Empate!'
        else:
            ponderacion = self.juego.calcular_ponderacion_x()
            mensaje = f'¡Jugador {ganador} gana con ponderación {ponderacion}!'
        texto = pygame.font.Font(None, 40).render(mensaje, True, (255, 255, 255))  # Texto blanco con tamaño de fuente reducido
        self.ventana.blit(texto, (self.tamaño_ventana // 2 - texto.get_width() // 2, self.tamaño_ventana // 2 - texto.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(5000)  # Espera 5 segundos antes de mostrar el gráfico
        self.juego.tablero.generar_grafico('tablero')
        self.juego.abrir_grafico('tablero.png')
        self.menu_activo = True

    def esperar_tecla(self): 
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.juego.guardar_q_table()
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                    esperando = False

    def dibujar_tablero(self): #Dibuja el estado actual del tablero
        for i in range(9):
            fila = i // 3
            columna = i % 3
            pygame.draw.rect(self.ventana, (255, 255, 255), pygame.Rect(columna * 200, fila * 200, 200, 200), 3)
            tablero_lista = self.juego.tablero.a_lista()
            if tablero_lista[i] == 'X':
                texto = self.fuente.render('X', True, (255, 0, 255))  # Color fuscia
                self.ventana.blit(texto, (columna * 200 + 100 - texto.get_width() // 2, fila * 200 + 100 - texto.get_height() // 2))
            elif tablero_lista[i] == 'O':
                texto = self.fuente.render('O', True, (64, 224, 208))  # Color turquesa
                self.ventana.blit(texto, (columna * 200 + 100 - texto.get_width() // 2, fila * 200 + 100 - texto.get_height() // 2))

    def manejar_eventos_menu(self):  #Manejo de eventos en el menu principal
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.juego.guardar_q_table()
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                for rect, opcion in self.opciones_rects:
                    if rect.collidepoint(x, y):
                        if "Jugar" in opcion:
                            self.menu_activo = False
                            self.juego_terminado = False
                            self.juego.reiniciar_tablero()
                        elif "Ver Historial" in opcion:
                            self.mostrar_historial()
                        elif "Ver Desarrollador" in opcion:
                            self.mostrar_desarrolladores()
                        elif "Salir" in opcion:
                            self.juego.guardar_q_table()
                            pygame.quit()
                            sys.exit()

    def manejar_eventos_juego(self): #Manejo de eventos durante el juego 
        while not self.juego_terminado:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.juego.guardar_q_table()
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = evento.pos
                    fila = y // 200
                    columna = x // 200
                    posicion = fila * 3 + columna
                    if not self.juego_terminado: 
                        if self.juego.realizar_movimiento(posicion):
                            self.dibujar_tablero()
                            pygame.display.flip()
                            pygame.time.wait(3000)  # Espera 3 segundos antes de mostrar el mensaje de ganador
                            self.juego_terminado = True
                            self.mostrar_ganador(self.juego.jugador)
                        else:
                            self.juego.movimiento_bot()
                            self.dibujar_tablero()
                            pygame.display.flip()
                            if self.juego.verificar_ganador():
                                pygame.time.wait(3000)  # Espera 3 segundos antes de mostrar el mensaje de ganador
                                self.juego_terminado = True
                                self.mostrar_ganador('O')
                            elif '-' not in self.juego.tablero.a_lista():
                                pygame.time.wait(3000)  # Espera 3 segundos antes de mostrar el mensaje de empate
                                self.juego_terminado = True
                                self.mostrar_ganador('Empate')
            if not self.juego_terminado:
                pygame.time.wait(100)

    def ejecutar(self): #Ejecuta el bucle principal del juego 
        while True:
            if self.menu_activo:
                self.mostrar_menu()
                self.manejar_eventos_menu()
            else:
                self.ventana.fill((0, 0, 0))  # Fondo negro
                self.dibujar_tablero()
                pygame.display.flip()
                self.manejar_eventos_juego()

# Ejecución del juego
juego = JuegoTikTakToe() #Instancia del juego
interfaz = InterfazTikTakToe(juego) #Instancia de la interfaz 
interfaz.ejecutar()  #Ejecuta el bucle principal 

