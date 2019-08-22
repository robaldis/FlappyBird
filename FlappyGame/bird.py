import neuralNetwork as nn

class Bird ():

    def __init__ (self, width, height, brain = None):
        self.x = int(200)
        self.y = int(400)
        self.size = int (10)
        self.gravity = 0.6
        self.lift = -10
        self.vel = 0

        self.score = 0
        self.pipeScore = 0
        self.fitness = 0

        self.bheight = 10
        self.bwidth = 10
        if brain == None:
            self.brain = nn.NeuralNetwrok(4, 4, 1, 0.1)
        else:
            self.brain = nn.NeuralNetwrok(oldBrain = brain)


        self.height = height
        self.width = width

    def up(self):
        self.vel = self.lift


    def think(self, pipes):
        closest = None
        closestD = 10000000
        for pipe in pipes:
            d = pipe.x - (self.x - 100)
            if d < closestD and d > 0:
                closest = pipe
                closestD = d


        input = []
        if (closest != None):
            # Inputs
            input.append(self.x - closest.x)
            input.append(self.y - closest.top)
            input.append(self.y - closest.bottom)
            input.append(self.vel)


        if (len(input) > 0):
            # Brain predicts if it should flap or not
            output = self.brain.predict(input)
        # To Flap or not to Flap
        if(output[0] > 0.5):
            self.up()
            pass


    def mutate(self, rate):
        self.brain.mutate(self.brain.weights_ho, rate)
        self.brain.mutate(self.brain.weights_ih, rate)
        self.brain.mutate(self.brain.bias_h, rate)
        self.brain.mutate(self.brain.bias_o, rate)



    def update(self):
        self.vel += self.gravity
        self.y += self.vel

        self.score += 1

        if (self.y >= self.height - self.bheight):
              self.y = self.height - self.bheight
              self.velocity = 0


        if (self.y <= self.bheight):
          self.y = self.bheight / 2
          self.velocity = 0

        pass
