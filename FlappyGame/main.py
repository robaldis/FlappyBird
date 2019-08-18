# ----------------------------------Imports-----------------------------------------------------
import pygame
from bird import Bird
from pipe import Pipe
import random
from numba import vectorize

#---Variables---
#--Constants--
# Size of the window
WIDTH = 600
HEIGHT = 700
# The size of the generation
GEN_SIZE = 200
# colour
BLUE = (0,0,255)
GREY = (30,30,30)
WHITE = (255,255,255)

#--Globals--
birds = list() # Hold the info for the birds that are ALIVE
savedBirds = list() # Hold the info for the birds that are DEAD

pipes = [] # Holds the info for all the pipes

highscore = 0 # contains the highscore
generation = 1 # What generation we are on

pcounter = 125 # counter for how oftern the pipes show up

F = None # holds the font


#---pygame init---

pygame.init() # Initialize all imported pygame modules
game_display = pygame.display.set_mode((WIDTH, HEIGHT)) # Display the window
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# setting up fonts with the size and type
FONT_28 = pygame.font.SysFont("Times New Roman, Arial", 28)
FONT_72 = pygame.font.SysFont("Times New Roman, Arial", 72)


#---Functaions---
def draw():
    # Globals
    global bird, pipes, pcounter, pipe, FONT_28, FONT_72, highscore, generation

    # fill the screen in grey
    game_display.fill((100,100,100))


    # Adding Pipes
    if (pcounter == 125):
        pcounter = 0
        pipes.append(Pipe(WIDTH, HEIGHT))
    pcounter += 1

    # FLAP
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        bird.up()

    # Update all the birds in the array
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
                continue

        # Check if the bird is going off the screen
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
        if (pipe.x < -150):
            pipes.remove(pipe)
        else:
            pipe.update()
            drawPipes(pipe)

    # Reset the game when there are no birds
    if (len(birds) == 0):
        resetGame()
        nextGeneration()


    # Go theough the birds and pipes to see if the birds have passed the pipe
    ## TODO: This doesnt seem to be verry efficient may want to change
    for bird in birds:
        for pipe in pipes:
            if bird.x > pipe.x and pipe.passed == False:
                pipe.scored(bird)
                highscore += 1

    # Sets up text to render onto the screen
    textHS =  FONT_28.render(f"Score: {highscore}", True, WHITE)
    textGen =  FONT_28.render(f"Generation Number: {generation}", True, WHITE)


    # Renders the text to the screen
    game_display.blit( textHS, (10,20))
    game_display.blit( textGen, (10,50))

    # Update the display
    pygame.display.update()

# Normalize the fitness
# set the fitness to between 0 and 1
def normalize(birds):
    for i in range(len(birds)):
        birds[i].score = pow(birds[i].score, 2)

# Get the fitness of the bird
# How well they done in the generation
def calculateFitness():
    sum = 0
    for bird in savedBirds:
        sum += bird.score

    for bird in savedBirds:
        bird.fitness = bird.score / sum

# Pick one of the birds from the savedBirds list
# This is done with probability acording to the fitness
def pickOne():
    fitness = 0
    index = 0
    bird = None
    r = random.random()
    while (r >  0):
        r = r - savedBirds[index].fitness
        index += 1

    # Go back one to get the index you want
    index -= 1
    bird = savedBirds[index]
    child = Bird(WIDTH,HEIGHT, bird.brain.copy()) # create a new bird with the the last bird brain
    # Mutate the childs brain
    child.mutate(0.2) # the probability that the weight will mutate
    return child # Return the child to add it to the list

# Create a new generation
def nextGeneration():
    # Globals
    global generation, savedBirds
    generation += 1 # Go to the next generation
    print (f"Generation Number: {generation}") # Show the new generation to the teminal

    normalize(savedBirds) # normalize fitness
    calculateFitness() # calculate how well the bird performed

    # Make a new generation
    for i in range(GEN_SIZE):
        birds.append(pickOne()) # create a new list of birds
    savedBirds = list() # empty the dead birds

def saveBird():
    global birds

    saveinfo = birds[0].brain
    # Save The file

# Draw the pipes
def drawPipes(pipes):
    pygame.draw.rect(game_display, GREY, [pipes.x, 0, pipes.w, pipes.top])
    pygame.draw.rect(game_display, GREY, [pipes.x, pipes.bottom, pipes.w, HEIGHT])
    pass

# Reset the game
def resetGame():
    global pcounter
    highscore = 0
    birds = list()
    pipes.clear()
    pipes.append(Pipe(WIDTH, HEIGHT))
    pcounter = 0


def main():
    # Globals
    global F, WIDTH, HEIGHT

    print (f"Generation Number: {generation}")


    # Start the first generation of birds
    for i in range(GEN_SIZE):
        birds.append(Bird(WIDTH, HEIGHT))

    # Keep the game running wile I am playing
    while True:
        for event in pygame.event.get():
            # Quit when pressed
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    # Save bird
                    saveBird()
        # Draw to the canvas
        draw()
        # Keep the refresh rate to
        clock.tick(240)

# Start program
if (__name__ == "__main__"):
    main()
