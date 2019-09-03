class TextElement():
    def __init__(self, font, text,x , y, colour = (0,0,0)):
        self.x = x
        self.y = y
        self.colour = colour
        self.text = text
        self.font = font


    def Draw(self, game_display):
        game_display.blit(self.font.render(self.text, True, self.colour), (self.x,self.y))


class ButtonElement():
    def __init__(self,font, text,x , y, size = (0,0), buttonColour = (0,0,0), textColour = (0,0,0)):
        self.x = x
        self.y = y
        self.width = size[1]
        self.height = size[0]
        self.buttonColour = buttonColour
        self.textColour = textColour
        self.text = text
        self.font = font


    def Draw(self, game_display):
        button = pygame.draw.rect(game_display, self.buttonColour, [self.x, self.y, self.width, self.height])
        text = self.font.render(self.text, True, self.textColour)
        # Moves the text to the center of the button
        offset = (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2))
        game_display.blit(text, offset)
