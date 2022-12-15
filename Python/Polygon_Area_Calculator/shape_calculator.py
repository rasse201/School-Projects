import math


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def get_area(self):
        return self.height * self.width

    def get_perimeter(self):
        return self.height * 2 + self.width * 2

    def get_diagonal(self):
        return (self.width ** 2 + self.height ** 2) ** 0.5

    def get_picture(self):
        if self.width > 50 or self.height > 50:
            return "Too big for picture."
        return ('*' * self.width + '\n') * self.height

    def get_amount_inside(self, shape):
        amount_inside_x = math.floor(self.width / shape.width)
        amount_inside_y = math.floor(self.height / shape.height)
        return amount_inside_x * amount_inside_y

    def __str__(self):
        return f"Rectangle(width={self.width}, height={self.height})"


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)
        self.side = side

    def set_height(self, height):
        self.height = height
        self.width = height
        self.side = height

    def set_width(self, width):
        self.height = width
        self.width = width
        self.side = width

    def set_side(self, side):
        self.height = side
        self.width = side
        self.side = side

    def __str__(self):
        return f"Square(side={self.side})"
