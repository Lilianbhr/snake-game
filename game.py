import pygame
pygame.init()
pygame.mixer.init()

# Taile des tuilles
nb_tuiles = 15
taille_tuiles = 32
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

# Boucle de jeu
running = True
while running :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    pygame.display.flip()
pygame.quit()