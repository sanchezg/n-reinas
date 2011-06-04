import time
import pygame
from pygame import *

class NReinas:
    """
    La clase NReinas se encarga de la logica del juego.
    """
    def __init__(self, tamanio = 8):
        self.tamanio            = tamanio
        self.ultimaColumna          = self.tamanio-1
        # columnas
        self.columnas          = self.tamanio * [-1]
        # diagonales, False es libre
        cantDiagonales     = 2 * self.tamanio - 1
        self.diagonales1       = cantDiagonales * [False]
        self.diagonales2      = cantDiagonales * [False]
        # lista de soluciones
        self.soluciones        = []

    # empezar
    def run(self):
        self.calcular(fila = 0, rangoColumnas = list(range(self.tamanio)))

    # busca y calcula las soluciones
    def calcular(self, fila, rangoColumnas):
        for col in rangoColumnas:
            # Calculo diagonales ...
            ixDiag1 = fila + col
            ixDiag2 = self.tamanio - 1 - fila + col

            # ...y compruebo que no esten ocupadas:
            if self.diagonales1[ixDiag1] or self.diagonales2[ixDiag2]:
		# un valor True indica que esa diagonal esta ocupada, salir
                continue

            # sino, ocuparlas:
            self.columnas[col]     = fila
            self.diagonales1[ixDiag1] = True
            self.diagonales2[ixDiag2] = True

            # Es la ultima columna?
            if fila == self.ultimaColumna:
                # Si, se encontraron todas las soluciones.
                self.soluciones.append(self.columnas[0:])
            else:
                # No, aplico recursividad para buscar la prox reina.
                self.calcular(fila + 1, self.remove(rangoColumnas[0:], col))

            # Al llegar aca aplicar backtracking, liberar diagonales...
            self.diagonales1[ixDiag1] = False
            self.diagonales2[ixDiag2] = False

    # devuelve el contenedor sin un valor determinado
    def remove(self, contenedor, valor):
        contenedor.remove(valor)
        return contenedor

class Gui:
    """
    La clase Gui se encarga de manejar los eventos de entrada
    y la salida por pantalla.
    """
    def __init__(self, tamanio = 8):
        self.tamanio = tamanio

    def main_loop(self):
        pygame.init()
        #self.model_entrada()

        while True:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT: return
                elif event.type == MOUSEBUTTONDOWN:
                    # aca poner el contador para el clock
                    (y,x) = pygame.mouse.get_pos()
                    if event.button == 1:
                        #poner reina
                        pass
                    elif event.button == 3:
                        #sacar reina
                        pass
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    #buscar soluciones al esquema
                    pass
            #actualizar screen
            pygame.display.flip()

    def model_entrada(self):
        self.screen = pygame.display.set_mode((268,271))
        pygame.display.set_caption('Damas al jaque - v0.5')
        self.screen.blit(carga_imagen('img/dama_fondo.jpg'),(0,0))

    def model_nuevo_juego(self):
        # modela la gui del juego nuevo (tablero)
        pygame.display.set_mode((HEIGHT,HEIGHT))
        c,f=0,0
        band=True
        for c in xrange(8):
            for f in xrange(8):
                if band:
                    self.set_cuadro('w', False, (c*LADO,f*LADO))
                    band=False
                else:
                    self.set_cuadro('b', False, (c*LADO,f*LADO))
                    band=True
            f=0
            band = not band #negar para que empiece con el otro color



def main():
    tamanio=int(raw_input("Ingrese el tamanio del tablero: "))

    miJuego = NReinas(tamanio)
    miGui = Gui(tamanio)
    miGui.main_loop()

    tinicio = time.time()
    miJuego.run()

    if False:
        # imprime en forma de vector las soluciones
        for solucion in miJuego.soluciones:
            vector = ""
            for ix in range(len(solucion)):
                vector += "(%d,%d)" % (ix+1, solucion[ix]+1)
            print(vector)
    print("... tiempo en seg: %f " % (time.time() - tinicio))
    print("... soluciones: %d " % (len(miJuego.soluciones)))

if __name__ == '__main__':
    main()

