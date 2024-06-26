import pygame
from sys import exit
import random


class Timberman():
    def __init__(self):
        self.game = True
        # Wczytanie obrazów postaci
        self.timberman1 = pygame.image.load('Assets/imgs/Player/Player0.png')
        self.timberman2 = pygame.image.load('Assets/imgs/Player/Player1.png')
        self.timberman3 = pygame.image.load('Assets/imgs/Player/Player2.png')

        # Skalowanie obrazu postaci
        self.timberman_surface = pygame.transform.scale2x(self.timberman1)

        # Uzyskanie prostokąta określającego pozycję postaci
        self.timberman_rect = self.timberman_surface.get_rect(topleft=(20, 550))

        # Flaga określająca, czy postać jest zwrócona w prawo
        self.facing_right = False

        # Aktualny obraz postaci
        self.timber_now = self.timberman1

        # Ustawienie początkowego wyniku
        self.score = 0

        # Inicjalizacja czcionki do wyświetlania wyniku
        self.font = pygame.font.Font('Assets/font/font.ttf', 50)
        self.text = self.font.render(str(self.score), True, (255, 255, 255))

    def draw(self):
        # Rysowanie postaci na ekranie
        screen.blit(self.timberman_surface, self.timberman_rect)

        # Wyświetlanie wyniku na środku ekranu
        screen.blit(self.text, self.text.get_rect(center=((screen.get_width() // 2), 200)))

    def K_LEFT(self):
        if self.game:
            # Zwiększenie wyniku i aktualizacja wyświetlanego tekstu
            self.score += 1
            self.text = self.font.render(str(self.score), True, (255, 255, 255))

            # Zmiana powierzchni postaci przy ruchu w lewo
            self.timberman_surface = pygame.transform.scale2x(self.timberman3)
            self.facing_right = False

            # Obracanie postaci w lewo jeśli była zwrócona w prawo
            if self.facing_right:
                self.timberman_surface = pygame.transform.flip(self.timberman_surface, True, False)
                self.facing_right = False

            # Ustawienie pozycji postaci na lewą stronę
            self.timberman_rect.topleft = (20, 550)

    def K_RIGHT(self):
        if self.game:
            # Zwiększenie wyniku i aktualizacja wyświetlanego tekstu
            self.score += 1
            self.text = self.font.render(str(self.score), True, (255, 255, 255))

            # Zmiana powierzchni postaci przy ruchu w prawo
            self.timberman_surface = pygame.transform.scale2x(self.timberman3)
            self.timberman_surface = pygame.transform.flip(self.timberman_surface, True, False)
            self.facing_right = True

            # Obracanie postaci w prawo jeśli była zwrócona w lewo
            if not self.facing_right:
                self.timberman_surface = pygame.transform.flip(self.timberman_surface, True, False)
                self.facing_right = True

            # Ustawienie pozycji postaci na prawą stronę
            self.timberman_rect.topleft = (340, 540)

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

    def check_collision(self, tree):
        # Sprawdzenie kolizji z pierwszą gałęzią
        if tree.branch_rects[0] is not None:
            if self.timberman_rect.colliderect(tree.branch_rects[0]):
                # Ustawienie gry na false, gdy dojdzie do kolizji
                self.game = False


class Tree():
    def __init__(self):
        # Wczytanie i skalowanie obrazów pni
        self.log_surface = pygame.image.load('Assets/imgs/Tree/Log0.png')
        self.log_surface = pygame.transform.scale2x(self.log_surface)

        # Ustawienie prostokąta dla pnia
        self.log_rect = self.log_surface.get_rect(center=(320, 619))

        # Lista pni
        self.log_list = [self.log_surface, self.log_surface, self.log_surface, self.log_surface, self.log_surface]

        # Wczytanie obrazów gałęzi i ich pozycjonowanie
        self.branch_left_surface = pygame.image.load('Assets/imgs/Tree/Branch.png')
        self.branch_left_rect = self.branch_left_surface.get_rect(center=(110, 550))
        self.branch_right_surface = pygame.image.load('Assets/imgs/Tree/Branch.png')
        self.branch_right_surface = pygame.transform.flip(self.branch_right_surface, True, False)

        # Losowe rozmieszczenie gałęzi
        self.branch_list = [None, None, None,
                            random.choice([None, self.branch_left_surface, self.branch_right_surface]),
                            random.choice([None, self.branch_left_surface, self.branch_right_surface]),
                            random.choice([None, self.branch_left_surface, self.branch_right_surface])]

        # Lista prostokątów dla gałęzi
        self.branch_rects = []

    def draw(self):
        # Czyszczenie listy prostokątów gałęzi
        self.branch_rects.clear()

        # Rysowanie pni drzewa na ekranie
        height = 761
        for log in self.log_list:
            rect = log.get_rect(center=(320, (height - 142)))
            screen.blit(log, rect)
            height -= 142

        # Rysowanie gałęzi na ekranie
        height = 834
        for branch in self.branch_list:
            if branch is not None:
                if branch == self.branch_left_surface:
                    rect = branch.get_rect(center=(110, (height - 142)))
                    if rect:
                        self.branch_rects.append(rect)
                    screen.blit(branch, rect)
                else:
                    rect = branch.get_rect(center=(530, (height - 142)))
                    if rect:
                        self.branch_rects.append(rect)
                    screen.blit(branch, rect)
                height -= 142
            else:
                height -= 142
                self.branch_rects.append(None)

    def click(self):
        # Usunięcie pierwszego elementu (gałęzi) z listy
        self.branch_list.pop(0)

        # Dodanie nowej gałęzi na końcu listy w zależności od ostatniej gałęzi
        if self.branch_list[-1] == self.branch_right_surface:
            self.branch_list.append(
                random.choice([None, None, self.branch_right_surface]))  # Zwiększenie szansy na None
        elif self.branch_list[-1] == self.branch_left_surface:
            self.branch_list.append(random.choice([None, None, self.branch_left_surface]))  # Zwiększenie szansy na None
        else:
            self.branch_list.append(random.choice([None, self.branch_left_surface, self.branch_right_surface]))


# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
screen = pygame.display.set_mode((640, 960))
pygame.display.set_caption("Hello World!")

# Wczytanie tła
sky_surface = pygame.image.load('Assets/imgs/Background/sky.png')
ground_surface = pygame.image.load('Assets/imgs/Background/Forest.png')

# Zegar do kontroli czasu
clock = pygame.time.Clock()

# Ustawienie timera do animacji postaci
timber_animation1 = pygame.USEREVENT + 1
pygame.time.set_timer(timber_animation1, 200)

# Utworzenie obiektu Timberman
timberman = Timberman()

# Utworzenie obiektu Tree
tree = Tree()

# Główna pętla gry
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if timberman.game:
            if event.type == timber_animation1:
                # Aktualizacja powierzchni postaci co 200 ms
                timberman.update_surface()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    timberman.K_LEFT()
                    tree.click()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    timberman.K_RIGHT()
                    tree.click()

    # Rysowanie tła
    if timberman.game:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 0))

        # Rysowanie drzewa
        tree.draw()

        # Rysowanie postaci
        timberman.draw()

        # Sprawdzenie kolizji postaci z gałęziami
        timberman.check_collision(tree)

    # Aktualizacja ekranu
    pygame.display.update()

    # Ustawienie liczby klatek na sekundę
    clock.tick(120)
