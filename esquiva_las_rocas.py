import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ancho, alto = 800, 600
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Esquiva las Rocas")

# Colores
color_pantalla = (0, 0, 0)

# Cargar la imagen del personaje
cohete_imagen = pygame.image.load("img/cohete.png")  # Imagen de cohete
cohete_imagen = pygame.transform.scale(cohete_imagen, (50, 50))  # Tamaño de cohete

# Cargar la imagen de la roca
roca_imagen = pygame.image.load("img/roca.png")  # Imagen de roca
roca_imagen = pygame.transform.scale(roca_imagen, (40, 40))  # Tamaño de rocas

# Posición del personaje
posicion_x = 400
posicion_y = 500

# Velocidades por nivel
velocidad_nivel_facil = 3
velocidad_nivel_medio = 5
velocidad_nivel_dificil = 7

# Velocidad del personaje
velocidad_cohete = 7  # Comienza con la velocidad del nivel fácil

# Rocas a esquivar
rocas = []
velocidad_rocas = velocidad_nivel_facil  # Comienza con la velocidad del nivel fácil

# Puntuación
puntuacion = 0
fuente = pygame.font.Font(None, 36)

# Tiempo para llevar el control del puntaje
incremento = pygame.time.get_ticks()
Intervalo_incremento = 2000  # 2000 ms (2 segundos)

# Reloj para controlar la velocidad del juego
reloj = pygame.time.Clock()

# Nivel de dificultad por defecto
nivel_dificultad = "Facil"

def mover_personaje():
    global posicion_x, velocidad_cohete  # Agrega la variable velocidad_cohete
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and posicion_x > 0:
        posicion_x -= velocidad_cohete
    if teclas[pygame.K_RIGHT] and posicion_x < ancho - 40:
        posicion_x += velocidad_cohete

def actualizar_rocas():
    global rocas, puntuacion
    for i in range(len(rocas)):
        x, y = rocas[i]
        y += velocidad_rocas
        rocas[i] = (x, y)
        rock_rect = pygame.Rect(x, y, 20, 20)
        if rock_rect.colliderect(pygame.Rect(posicion_x, posicion_y, 40, 40)):
            seleccionar_nivel()
            puntuacion = 0

    rocas = [(x, y) for x, y in rocas if y < alto]

def generar_rocas():
    if random.randint(0, 100) < 5:
        x = random.randint(0, ancho - 40)
        y = 0
        rocas.append((x, y))

def control_puntaje():
    global puntuacion, incremento
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - incremento >= Intervalo_incremento:
        puntuacion += 1
        incremento = tiempo_actual

def mostrar_pantalla():
    pantalla.fill(color_pantalla)
    pantalla.blit(cohete_imagen, (posicion_x, posicion_y))
    for x, y in rocas:
        pantalla.blit(roca_imagen, (x, y))
    mostrar_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, (255, 0, 0))
    mostrar_menu = fuente.render("M: Menu", True, (255, 0, 0))
    mostrar_salir = fuente.render("X: Salir", True, (255, 0, 0))
    
    pantalla.blit(mostrar_puntuacion, (10, 10))
    pantalla.blit(mostrar_menu, (10, 50))  # Muestra el texto "Salir" debajo de la puntuación
    pantalla.blit(mostrar_salir, (10, 90))  # Muestra el texto "menu" debajo de la puntuación
    pygame.display.flip()

def seleccionar_nivel():
    global velocidad_rocas, nivel_dificultad
    #global velocidad_rocas, velocidad_cohete, nivel_dificultad
    seleccionado = False
    while not seleccionado:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    velocidad_rocas = velocidad_nivel_facil
                    #velocidad_cohete = velocidad_nivel_facil
                    nivel_dificultad = "Facil"
                    seleccionado = True
                elif event.key == pygame.K_2:
                    velocidad_rocas = velocidad_nivel_medio
                    #velocidad_cohete = velocidad_nivel_medio
                    nivel_dificultad = "Medio"
                    seleccionado = True
                elif event.key == pygame.K_3:
                    velocidad_rocas = velocidad_nivel_dificil
                    #velocidad_cohete = velocidad_nivel_dificil
                    nivel_dificultad = "Dificil"
                    seleccionado = True
                elif event.key == pygame.K_x:
                    pygame.display.flip()
                    pygame.quit()
                    sys.exit()

        pantalla.fill(color_pantalla)
        mensaje = fuente.render("Selecciona el nivel:", True, (255, 0, 0))
        facil = fuente.render("1 - Fácil", True, (255, 0, 0))
        medio = fuente.render("2 - Medio", True, (255, 0, 0))
        dificil = fuente.render("3 - Difícil", True, (255, 0, 0))
        salir = fuente.render("X - Salir", True, (255, 0, 0))

        pantalla.blit(mensaje, (ancho // 2 - 100, alto // 2 - 80))
        pantalla.blit(facil, (ancho // 2 - 100, alto // 2 - 40))
        pantalla.blit(medio, (ancho // 2 - 100, alto // 2))
        pantalla.blit(dificil, (ancho // 2 - 100, alto // 2 + 40))
        pantalla.blit(salir, (ancho // 2 - 100, alto // 2 + 80))
        pygame.display.flip()

# Seleccionar nivel antes de iniciar el juego
seleccionar_nivel()

# Definir función de juego
def jugar_juego():
    global correr_juego, puntuacion
    correr_juego = True
    while correr_juego:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                correr_juego = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    pygame.quit()
                    sys.exit()  # Salir del juego con la tecla "x"
                elif event.key == pygame.K_m:
                    seleccionar_nivel()  # Regresar al menú con la tecla "m"
                    puntuacion = 0  # Reiniciar la puntuación al volver al menú

        mover_personaje()
        actualizar_rocas()
        generar_rocas()
        control_puntaje()
        mostrar_pantalla()
        reloj.tick(30)

# Lanzar el juego
jugar_juego()

# Finalizar Pygame
pygame.quit()
sys.exit()
