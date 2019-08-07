import pygame
from bird import Bird
from pipe import Pipe
import random

WIDTH = 600
HEIGHT = 700

GEN_SIZE = 100

BLUE = (0,0,255)
GREY = (30,30,30)

game_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

birds = list()
savedBirds = list()
pipes = []

pcounter = 125


# Start the first generation of birds
for i in range(GEN_SIZE):
    birds.append(Bird(WIDTH, HEIGHT))



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

    # Update All the birds
    for bird in birds:
        # Updating the bird
        bird.update()
        # AI for the bird
        bird.think(pipes)
        # Draw the bird
        pygame.draw.circle(game_display, BLUE, (int(bird.x), int(bird.y)), bird.size)

        # For each bird check each pipe to see if it has hit
        for pipe in pipes:
            if (pipe.scored(bird)):
                print("Scored")

            if (pipe.hits(bird)):
                # Remove the bird from the list
                savedBirds.append(bird)
                birds.remove(bird)
                continue #
        if bird.y > HEIGHT - 20:
            if (bird):
                # Remove the bird from the list
                savedBirds.append(bird)
                birds.remove(bird)

    # Update and draw pipes
    for pipe in pipes:
        pipe.update()
        drawPipes(pipe)




    if (len(birds) == 0):
        resetGame()
        nextGeneration()

    # Update the display
    pygame.display.update()
    pass


def calculateFitness():
    sum = 0
    for bird in savedBirds:
        sum += bird.score
        print(f"score {bird.score}")

    print(f"this is the sum {sum}")
    for bird in savedBirds:
        bird.fitness += bird.score / sum


def pickOne():
    fitness = 0
    bird = None
    for sbird in savedBirds:
        if sbird.fitness > fitness:
            fitness = sbird.fitness
            bird = sbird
    child = Bird(WIDTH,HEIGHT, bird.brain)
    #child.mutate(random.uniform(0,0.1))

    return child


def nextGeneration():

    calculateFitness()

    # Make a new generation
    for i in range(GEN_SIZE):
        birds.append(pickOne())
    savedBirds = list()


def drawPipes(pipes):
    pygame.draw.rect(game_display, GREY, [pipes.x, 0, pipes.w, pipes.top])
    pygame.draw.rect(game_display, GREY, [pipes.x, pipes.bottom, pipes.w, HEIGHT])
    pass


def resetGame():
    global pcounter
    birds = list()
    pipes.clear()
    pipes.append(Pipe(WIDTH, HEIGHT))
    pcounter = 0




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
