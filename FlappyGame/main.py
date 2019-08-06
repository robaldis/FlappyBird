import pygame
import bird
from pipe import Pipe

WIDTH = 600
HEIGHT = 800

BLUE = (0,0,255)
GREY = (30,30,30)

game_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

bird = bird.Bird(WIDTH, HEIGHT)
pipes = []


pcounter = 100


def draw():
    global bird, pipes, pcounter, pipe
    game_display.fill((100,100,100))

    # Adding Pipes
    if (pcounter == 125):
        pcounter = 0
        pipes.append(Pipe(WIDTH, HEIGHT))
    pcounter += 1

    # FLAP
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        bird.up()

    # Updating the bird
    bird.update()
    # Draw the bird
    pygame.draw.circle(game_display, BLUE, (int(bird.x), int(bird.y)), bird.size)



    # Update and draw pipes
    for pipe in pipes:
        if (pipe.hits(bird)):
            print ("Dead")


        pipe.update()
        drawPipes(pipe)


    # Update the display
    pygame.display.update()
    pass


def drawPipes(pipes):
    pygame.draw.rect(game_display, GREY, [pipes.x, 0, pipes.w, pipes.top])
    pygame.draw.rect(game_display, GREY, [pipes.x, pipes.bottom, pipes.w, HEIGHT])


    #pygame.draw.rect(game_display, GREY, [pipes.top, pipes.x, WIDTH, pipes.w])
    pass


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Draw to the canvas
        draw()
        # Keep the refresh rate to 60
        clock.tick(60)



if (__name__ == "__main__"):
    main()
