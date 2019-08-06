import neuralNetowrk as nn

class Bird ():

    def __init__ (self, width, height):
        self.x = int(200)
        self.y = int(400)
        self.size = int (10)
        self.gravity = 0.6
        self.lift = -10
        self.vel = 0
        self.score = 0

        self.bheight = 10
        self.bwidth = 10

        self.brain = nn.neuralNetowrk(2,2,1)


        self.height = height
        self.width = width

    def up(self):
        self.vel = self.lift



    def update(self):
        self.vel += self.gravity
        self.y += self.vel

        if (self.y >= self.height - self.bheight):
              self.y = self.height - self.bheight
              self.velocity = 0


        if (self.y <= self.bheight):
          self.y = self.bheight / 2
          self.velocity = 0

        pass
