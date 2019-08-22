import random

class Pipe(object):

    def __init__(self, width, height, GEN_SIZE):
        self.spacing = 120
        self.top = random.randint(int(height / 6),int( 3 / 4* height))
        self.bottom = self.top + self.spacing

        self.x = width
        self.w = 80
        self.speed = 3
        self.passed = list()
        for i in range (GEN_SIZE):
            self.passed.append(False)
        self.highlight = False




    def hits(self, bird):
        halfBirdHeight = bird.height
        halfBirdWidth = bird.width

        if bird.y < self.top or bird.y > self.bottom:
            #if self.w is huge, then we need different collision model
            if bird.x > self.x and bird.x < self.x + self.w:
                #self.highlight = True
                #self.passed = True
                return True
        else:
            #self.highlight = False
            return False


    def scored(self, bird):
            #self.passed = True
            pass


    def update(self):
        self.x -= self.speed

    def offscreen():
        return (self.x < -self.w)
