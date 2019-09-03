#---Imports---
import pygame
from lib.bird import Bird
from lib.pipe import Pipe
from lib.HUD import *
from lib.GeneticAlgorithm import *
import random
import json
import numpy as np

# Size of the window
WIDTH = 600
HEIGHT = 700
# The size of the generation
GEN_SIZE = 200
# Colour
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

        self.GA = GeneticAlgorithm(GEN_SIZE, WIDTH, HEIGHT)

        self.highscore = 0
        self.generation = 1

        # setting up fonts with the size and type
        self.FONT_28 = pygame.font.SysFont("Times New Roman, Arial", 28)
        self.FONT_72 = pygame.font.SysFont("Times New Roman, Arial", 72)

        # This holds all the hud elements by name
        self.HUD = {}

        self.text = [None] * 3
        # Sets up text to render onto the screen
        self.HUD["score"] = TextElement(self.FONT_28, "", 10, 20, WHITE)
        self.HUD["generation"] = TextElement(self.FONT_28, "", 10,50, WHITE)
        self.HUD["population"] = TextElement(self.FONT_28, "", 10, 90, WHITE)
        self.HUD["info1"] = TextElement(self.FONT_28,"To save a bird press S", 10, HEIGHT - 110, GREY)
        self.HUD["info2"] = TextElement(self.FONT_28, "To load a bird brain press R", 10, HEIGHT - 70, GREY)
        #self.HUD["Button"] = ButtonElement(self.FONT_28, "Button", 100, 100, (50, 200), WHITE, GREY)

    def Draw(self):
        # fill the screen in grey
        self.game_display.fill((0,0,0))

        # Update all the birds
        for bird in self.birds:
            bird.think(self.pipes)
            bird.update()
            # Draw the bird
            pygame.draw.circle(self.game_display, BLUE, (int(bird.x), int(bird.y)), bird.size)

        # Adding Pipes to the screen
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
            self.birds = self.GA.nextGeneration(self.savedBirds, self.birds)

        self.highscore = self.birds[0].pipeScore

        # Update HUD
        self.HUD["score"].text = f"Score: {self.highscore}"
        self.HUD["generation"].text = f"Generation Number: {self.generation}"
        self.HUD["population"].text = f"Generation Population: {len(self.birds)}"

        # Draw All the text
        for index, item  in self.HUD.items():
            item.Draw(self.game_display)

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
                # Hits the pipe
                if (pipe.hits(bird) and hit == False):
                    self.savedBirds.append(bird)
                    hit = True
                    self.birds.remove(bird)
            index += 1


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


#---pygame init---

pygame.init() # Initialize all imported pygame modules
game_display = pygame.display.set_mode((WIDTH, HEIGHT)) # Display the window
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

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
                    game.GA.saveBird(game.birds)
                if event.key == pygame.K_r:
                    # Read the brid brain
                    game.resetGame(False, game.GA.readBird())

        # Draw to the canvas
        game.Draw()
        # Keep the refresh rate to
        clock.tick(1024)

# Start program
if (__name__ == "__main__"):
    main(game_display, WIDTH, HEIGHT)
