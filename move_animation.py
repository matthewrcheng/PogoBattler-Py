# import circle
from pygame.draw import circle

class MoveAnimationHandler:

    def __init__(self, screen, move, start, end, direction = 'left', steps=20, radius=10) -> None:
        self.screen = screen
        self.color = self.pick_color(move.type.lower())
        self.start = start
        self.end = end
        self.direction = direction
        self.current_x = self.start[0]
        self.current_y = self.start[1]
        self.step_size = int((self.end[0] - self.start[0]) / steps)
        self.radius = radius

    def get_next_position(self):
        if self.direction == 'left':
            if self.current_x >= self.end[0]:
                return True
        else:
            if self.current_x <= self.end[0]:
                return True
        self.current_x += self.step_size
        return False

    def get_image(self):
        if self.get_next_position():
            return None
        
        return circle(self.screen, self.color, (self.current_x, self.current_y), self.radius)

    def pick_color(self, type):
        if type == "fire":
            return (243, 104, 8)
        elif type == "water":
            return (8, 145, 243)
        elif type == "grass":
            return (56, 186, 22)
        elif type == "electric":
            return (240, 240, 28)
        elif type == "psychic":
            return (232, 27, 198)
        elif type == "ice":
            return (172, 237, 243)
        elif type == "dragon":
            return (22, 54, 236)
        elif type == "fairy":
            return (255, 132, 241)
        elif type == "fighting":
            return (157, 10, 10)
        elif type == "normal":
            return (210, 210, 210)
        elif type == "ghost":
            return (121, 16, 175)
        elif type == "ground":
            return (244, 210, 113)
        elif type == "flying":
            return (119, 200, 239)
        elif type == "poison":
            return (182, 51, 200)
        elif type == "bug":
            return (135, 200, 51)
        elif type == "rock":
            return (160, 106, 53)
        elif type == "steel":
            return (142, 142, 142)
        elif type == "dark":
            return (30, 30, 30)
        else:
            return (0, 0, 0)
        
