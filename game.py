import pygame
pygame.init()
pygame.mixer.init()

# Taile des tuilles
nb_tuiles = 15
taille_tuiles = 40
score_hauteur = 32

# Couleures
couleurs = {
    "vert" : pygame.color.Color(0, 255, 0),
    "noir" : pygame.color.Color(0, 0, 0),
    "blanc" : pygame.color.Color(255, 255, 255)
}

# Fenêtre
largeur = nb_tuiles * taille_tuiles
hauteur = nb_tuiles * taille_tuiles + score_hauteur
screen = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Snake")
screen.fill(couleurs["vert"])

# Musique
musique = pygame.mixer.music.load("assets/music/music.mp3")
pygame.mixer.music.play()

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img_tetes = {
            "H" : pygame.image.load("assets/images/head_up.png").convert_alpha(),
            "B": pygame.image.load("assets/images/head_down.png").convert_alpha(),
            "D": pygame.image.load("assets/images/head_right.png").convert_alpha(),
            "G": pygame.image.load("assets/images/head_left.png").convert_alpha()
        }
        self.direction = "D"
        self.tete = self.img_tetes[self.direction]
        self.image = self.tete
        self.rect = self.image.get_rect()
        self.rect.x = (nb_tuiles/2) * taille_tuiles
        self.rect.y = (nb_tuiles/2) * taille_tuiles
        self.taille = 3
        self.liste_pos = []

    def draw(self):
        screen.blit(self.tete, self.rect)

class Body(pygame.sprite.Sprite):
    def __init__(self, liste_de_positions):
        super().__init__()
        self.images = []
        self.liste = liste_de_positions

    def choisir_image(self):
        for t in range(len(self.liste)) :
            if self.liste[t] == self.liste[0] :
                if self.liste[t][0] > self.liste[1][0]:
                    self.images.append(pygame.image.load("assets/images/tail_right.png").convert_alpha())
                elif self.liste[t][0] < self.liste[1][0]:
                    self.images.append(pygame.image.load("assets/images/tail_left.png").convert_alpha())
                elif self.liste[t][1] > self.liste[1][1]:
                    self.images.append(pygame.image.load("assets/images/tail_up.png").convert_alpha())
                elif self.liste[t][1] < self.liste[1][1]:
                    self.images.append(pygame.image.load("assets/images/tail_down.png").convert_alpha())
            else :
                if self.liste[t][0] > self.liste[t - 1][0]:
                    if self.liste[t][1] > self.liste[t + 1][1]:
                        self.images.append(pygame.image.load("assets/images/body_topleft.png").convert_alpha())
                    elif self.liste[t][1] < self.liste[t + 1][1]:
                        self.images.append(pygame.image.load("assets/images/body_bottomleft.png").convert_alpha())
                    else :
                        self.images.append(pygame.image.load("assets/images/body_horizontal.png").convert_alpha())
                elif self.liste[t][0] < self.liste[t - 1][0]:
                    if self.liste[t][1] > self.liste[t + 1][1]:
                        self.images.append(pygame.image.load("assets/images/body_topright.png").convert_alpha())
                    elif self.liste[t][1] < self.liste[t + 1][1]:
                        self.images.append(pygame.image.load("assets/images/body_bottomright.png").convert_alpha())
                    else :
                        self.images.append(pygame.image.load("assets/images/body_horizontal.png").convert_alpha())
                elif self.liste[t][1] > self.liste[t - 1][1]:
                    if self.liste[t][0] > self.liste[t + 1][0]:
                        self.images.append(pygame.image.load("assets/images/body_topleft.png").convert_alpha())
                    elif self.liste[t][0] < self.liste[t + 1][0]:
                        self.images.append(pygame.image.load("assets/images/body_topright.png").convert_alpha())
                    else :
                        self.images.append(pygame.image.load("assets/images/body_vertical.png").convert_alpha())
                elif self.liste[t][1] < self.liste[t - 1][1]:
                    if self.liste[t][0] > self.liste[t + 1][0]:
                        self.images.append(pygame.image.load("assets/images/body_bottomleft.png").convert_alpha())
                    elif self.liste[t][0] < self.liste[t + 1][0]:
                        self.images.append(pygame.image.load("assets/images/body_bottomright.png").convert_alpha())
                    else :
                        self.images.append(pygame.image.load("assets/images/body_vertical.png").convert_alpha())


snake = Snake()

# Boucle de jeu
clock = pygame.time.Clock()
running = True
while running :
    snake.liste_pos.append((snake.rect.x, snake.rect.y))
    if len(snake.liste_pos) > snake.taille :
        snake.liste_pos.remove(snake.liste_pos[0])
    screen.fill(couleurs["vert"])
    snake.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP and snake.direction != 'B':
                snake.direction = 'H'
                snake.tete = snake.img_tetes[snake.direction]
            elif event.key == pygame.K_DOWN and snake.direction != 'H':
                snake.direction = 'B'
                snake.tete = snake.img_tetes[snake.direction]
            elif event.key == pygame.K_RIGHT and snake.direction != 'G':
                snake.direction = 'D'
                snake.tete = snake.img_tetes[snake.direction]
            elif event.key == pygame.K_LEFT and snake.direction != 'D':
                snake.direction = 'G'
                snake.tete = snake.img_tetes[snake.direction]
    if snake.direction == "H" :
        snake.rect.y -= taille_tuiles
    elif snake.direction == "B" :
        snake.rect.y += taille_tuiles
    elif snake.direction == "D" :
        snake.rect.x += taille_tuiles
    elif snake.direction == "G" :
        snake.rect.x -= taille_tuiles
    pygame.display.flip()
    clock.tick(7)
pygame.quit()