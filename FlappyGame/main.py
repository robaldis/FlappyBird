import pygame
from bird import Bird
from pipe import Pipe
import random
from numba import vectorize

WIDTH = 600
HEIGHT = 700

GEN_SIZE = 200

BLUE = (0,0,255)
GREY = (30,30,30)

game_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

birds = list()
savedBirds = list()
pipes = []

generation = 1
print (f"Generation Number: {generation}")

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

    # pygame.draw.circle(game_display, BLUE, (int(birds[0].x), int(birds[0].y)), birds[0].size)
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
            if (pipe.hits(bird)):
                # Remove the bird from the list
                savedBirds.append(bird)
                birds.remove(bird)
                continue #
        if bird.y > HEIGHT - 20:
            # Remove the bird from the list
            savedBirds.append(bird)
            try:
                birds.remove(bird)
            except:
                continue
        if bird.y < (0 + 20):
            # Remove the bird from the list
            savedBirds.append(bird)
            try:
                birds.remove(bird)
            except:
                continue

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


def normalize(birds):
    for i in range(len(birds)):
        birds[i].score = pow(birds[i].score, 2)


def calculateFitness():
    sum = 0
    for bird in savedBirds:
        sum += bird.score

    for bird in savedBirds:
        bird.fitness = bird.score / sum

def pickOne():
    fitness = 0
    index = 0
    bird = None
    r = random.random()
    while (r >  0):
        r = r - savedBirds[index].fitness
        index += 1


    for b in savedBirds:
        if (fitness < b.fitness):
            fitness = b.fitness
            bird = b
    index -= 1
    # bird = savedBirds[index]
    child = Bird(WIDTH,HEIGHT, bird.brain.copy())
    #print (child.brain.weights_ho)
    child.mutate(0.2)
    #print (child.brain.weights_ho)

    return child

def nextGeneration():
    global generation, savedBirds
    generation += 1
    print (f"Generation Number: {generation}")


    # normalize(savedBirds)
    calculateFitness()

    # Make a new generation
    for i in range(GEN_SIZE):
        birds.append(pickOne())
    savedBirds = list()
    #for i in range (len(birds)):
        #birds[i].mutate()


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
