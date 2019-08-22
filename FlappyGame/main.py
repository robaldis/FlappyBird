# ----------------------------------Imports-----------------------------------------------------
import pygame
from bird import Bird
from pipe import Pipe
import random
import json
import numpy as np

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


class Game ():
    def __init__(self, game_display):

        self.game_display = game_display

        self.pipeRate = 0
        self.pipes = list()
        self.birds = list()
        self.savedBirds = list()

        # Scoring
        self.highscore = 0
        self.generation = 1

        # setting up fonts with the size and type
        self.FONT_28 = pygame.font.SysFont("Times New Roman, Arial", 28)
        self.FONT_72 = pygame.font.SysFont("Times New Roman, Arial", 72)

        self.HUD = HUDElements()

        self.text = [None] * 3
        # Sets up text to render onto the screen
        self.HUD.addElement("score", ScreenElement("", 10, 20, element = "text"))
        self.HUD.addElement("generation", ScreenElement("", 10,50, element = "text"))
        self.HUD.addElement("population", ScreenElement("", 10, 90, element = "text"))
        self.HUD.addElement("info1", ScreenElement(self.FONT_28.render("To save a bird press S", True, GREY), 10, HEIGHT - 110, element = "text"))
        self.HUD.addElement("info2", ScreenElement(self.FONT_28.render("To load a bird brain press R", True, GREY), 10, HEIGHT - 70, element = "text"))

        # self.HUD.addElement("Button", ScreenElement(self.FONT_28.render("QUIT", False, WHITE), 10, HEIGHT - 90, (170, 80), (0,66,99), "Button"))

    def Draw(self):
        # fill the screen in grey
        self.game_display.fill((0,0,0))


        # --Update all the birds--
        for bird in self.birds:
            bird.think(self.pipes)
            bird.update()
            # Draw the bird
            pygame.draw.circle(self.game_display, BLUE, (int(bird.x), int(bird.y)), bird.size)


        # Adding Pipes
        if (self.pipeRate == 125):
            self.pipeRate = 0
            self.pipes.append(Pipe(WIDTH, HEIGHT, GEN_SIZE))
        self.pipeRate += 1

        # Update all the pipes
        for pipe in self.pipes:
            if (pipe.x < -150):
                self.pipes.remove(pipe)
            else:
                pipe.update()
                self.drawPipes(pipe)

        # Check all the collisions
        self.checkCollision()

        # Reset the game when there are no birds
        if (len(self.birds) == 0):
            self.resetGame()
            self.birds = nextGeneration(self.generation, self.savedBirds, self.birds)

        self.highscore = self.birds[0].pipeScore

        # Update HUD
        self.HUD.Get()["score"].text = self.FONT_28.render(f"Score: {self.highscore}", True, WHITE)
        self.HUD.Get()["generation"].text = self.FONT_28.render(f"Generation Number: {self.generation}", True, WHITE)
        self.HUD.Get()["population"].text = self.FONT_28.render(f"Generation Population: {len(self.birds)}", True, WHITE)



        # Draw All the text
        for index, item  in self.HUD.Get().items():
            item.DrawText(self.game_display)


        # Update the display
        pygame.display.update()


    # Draw the pipes
    def drawPipes(self, pipes):
        pygame.draw.rect(self.game_display, GREY, [pipes.x, 0, pipes.w, pipes.top])
        pygame.draw.rect(self.game_display, GREY, [pipes.x, pipes.bottom, pipes.w, HEIGHT])
        pass


    def checkCollision(self):
        index = 0

        # --Check for collision--
        for bird in list(self.birds):
            hit = False
            # Hit the bottom
            if (bird.y > HEIGHT - 20 and hit == False):
                self.savedBirds.append(bird)
                self.birds.remove(bird)
                hit = True

            # Hit the top
            if (bird.y < (0 + 20) and hit == False):
                self.savedBirds.append(bird)
                self.birds.remove(bird)
                hit = True

            for pipe in list(self.pipes):
                # Gone through the gate
                if (bird.x > pipe.x and pipe.passed[index] == False):
                    pipe.scored(bird)
                    bird.pipeScore += 1
                    pipe.passed[index] = True

                if (pipe.hits(bird) and hit == False):
                    self.savedBirds.append(bird)
                    hit = True
                    self.birds.remove(bird)
            index   += 1


    # Reset the game
    def resetGame(self, training = True, jsonData= None):
        self.highscore = 0
        self.generation += 1
        self.birds = list()
        self.pipes.clear()
        self.pipes.append(Pipe(WIDTH, HEIGHT, GEN_SIZE))
        self.pipeRate = 0



        if (training == False):
            self.birds.append(Bird(WIDTH,HEIGHT,jsonData))
            self.generation = 0


class ScreenElement():
    def __init__(self, text,x , y, size = (0,0), colour = (0,0,0,0), element = ""):
        self.element = element
        self.x = x
        self.y = y
        self.width = size[0]
        self.height = size[1]
        self.colour = colour
        self.text = text


    def DrawText(self, game_display):
        if (self.element == "text"):
            game_display.blit(self.text, (self.x,self.y))
        elif (self.element ==  "Button"):
            button = pygame.draw.rect(game_display, self.colour, [self.x, self.y, self.width, self.height])
            game_display.blit(self.text, button.center)

class HUDElements():
    def __init__(self):
        self.dict = {}

    def addElement(self, Key, Element):
        self.dict[Key] = Element

    def Get(self):
        return self.dict


#---pygame init---

pygame.init() # Initialize all imported pygame modules
game_display = pygame.display.set_mode((WIDTH, HEIGHT)) # Display the window
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()


# Normalize the fitness
# set the fitness to between 0 and 1
def normalize(birds):
    for i in range(len(birds)):
        birds[i].score = pow(birds[i].score, 2)

# Get the fitness of the bird
# How well they done in the generation
def calculateFitness(savedBirds):
    sum = 0
    for bird in savedBirds:
        sum += bird.score

    for bird in savedBirds:
        bird.fitness = bird.score / sum

# Pick one of the birds from the savedBirds list
# This is done with probability acording to the fitness
def pickOne(savedBirds):
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
def nextGeneration(generation, savedBirds, birds):
    normalize(savedBirds) # normalize fitness
    calculateFitness(savedBirds) # calculate how well the bird performed

    # Make a new generation
    for i in range(GEN_SIZE):
        birds.append(pickOne(savedBirds)) # create a new list of birds

    return birds

def saveBird(birds):
    saveinfo = birds[0].brain
    dict = {
            "weights_ih" : saveinfo.weights_ih.tolist(),
            "weights_ho" : saveinfo.weights_ho.tolist(),
            "bias_h" : saveinfo.bias_h.tolist(),
            "bias_o" : saveinfo.bias_o.tolist(),
    }
    # Writing JSON data
    with open("BestBirdBrain.json", 'w') as f:
        json.dump(dict, f, indent = 4)


def readBird():
    with open("BestBirdBrain.json", "r") as f:
        jsonData = json.load(f)
    return jsonData


def main(game_display, WIDTH, HEIGHT):
    game = Game(game_display)

    # Start the first generation of birds
    for i in range(GEN_SIZE):
        game.birds.append(Bird(WIDTH, HEIGHT))
    game.pipes.append(Pipe(WIDTH,HEIGHT, GEN_SIZE))

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
                    saveBird(game.birds)
                if event.key == pygame.K_r:
                    # Read the brid brain
                    game.resetGame(False, readBird())

        # Draw to the canvas
        game.Draw()
        # Keep the refresh rate to
        clock.tick(1024)

# Start program
if (__name__ == "__main__"):
    main(game_display, WIDTH, HEIGHT)
