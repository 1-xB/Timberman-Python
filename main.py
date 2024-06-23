import pygame
from sys import exit


class Timberman():
    def __init__(self):
        # Wczytanie obrazów postaci
        self.timberman1 = pygame.image.load('Player0.png')
        self.timberman2 = pygame.image.load('Player1.png')

        # Skalowanie obrazu postaci
        self.timberman_surface = pygame.transform.scale2x(self.timberman1)

        # Uzyskanie prostokąta określającego pozycję postaci
        self.timberman_rect = self.timberman_surface.get_rect(topleft=(20, 530))

        # Flaga określająca, czy postać jest zwrócona w prawo
        self.facing_right = False

        # Aktualny obraz postaci
        self.timber_now = self.timberman1

    def draw(self):
        # Rysowanie postaci na ekranie
        screen.blit(self.timberman_surface, self.timberman_rect)

    def K_LEFT(self):
        # Obracanie postaci w lewo
        if self.facing_right:
            self.timberman_surface = pygame.transform.flip(self.timberman_surface, True, False)
            self.facing_right = False

        # Ustawienie pozycji postaci na lewą stronę
        self.timberman_rect.topleft = (20, 530)

    def K_RIGHT(self):
        # Obracanie postaci w prawo
        if not self.facing_right:
            self.timberman_surface = pygame.transform.flip(self.timberman_surface, True, False)
            self.facing_right = True

        # Ustawienie pozycji postaci na prawą stronę
        self.timberman_rect.topleft = (340, 530)

    def update_surface(self):
        # Aktualizacja powierzchni postaci do animacji
        if self.timber_now == self.timberman1:
            # Zmiana obrazu na timberman2
            self.timberman_surface = pygame.transform.scale2x(self.timberman2)
            if self.facing_right:
                self.timberman_surface = pygame.transform.flip(self.timberman_surface, True, False)
            self.timber_now = self.timberman2
        elif self.timber_now == self.timberman2:
            # Zmiana obrazu na timberman1
            self.timberman_surface = pygame.transform.scale2x(self.timberman1)
            if self.facing_right:
                self.timberman_surface = pygame.transform.flip(self.timberman_surface, True, False)
            self.timber_now = self.timberman1


# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
screen = pygame.display.set_mode((640, 960))
pygame.display.set_caption("Hello World!")

# Wczytanie tła
sky_surface = pygame.image.load('sky.png')
ground_surface = pygame.image.load('Forest.png')

# Zegar do kontroli czasu
clock = pygame.time.Clock()

# Ustawienie timera do animacji postaci
timber_animation1 = pygame.USEREVENT + 1
pygame.time.set_timer(timber_animation1, 500)

# Utworzenie obiektu Timberman
timberman = Timberman()

# Główna pętla gry
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == timber_animation1:
            # Aktualizacja powierzchni postaci co 500 ms
            timberman.update_surface()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                timberman.K_LEFT()
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                timberman.K_RIGHT()

    # Rysowanie tła
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 0))

    # Rysowanie postaci
    timberman.draw()

    # Aktualizacja ekranu
    pygame.display.update()

    # Ustawienie liczby klatek na sekundę
    clock.tick(60)
