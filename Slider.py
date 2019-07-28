import pygame
import gc


def mapRange(val, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((val - istart) / (istop - istart))


def rect(surface, color, rect, width=0):
    xposition = rect[0]
    yposition = rect[1]
    widthrect = rect[2]
    heightrect = rect[3]
    pygame.draw.line(surface, color, (xposition - int(width / 2.00000000001),
                                      yposition), (xposition + widthrect + width // 2, yposition), width)
    pygame.draw.line(surface, color, (xposition + widthrect, yposition),
                     (xposition + widthrect, yposition + heightrect + width // 2), width)
    pygame.draw.line(surface, color, (xposition, yposition + heightrect),
                     (xposition + widthrect + width // 2, yposition + heightrect), width)
    pygame.draw.line(surface, color, (xposition, yposition),
                     (xposition, yposition + heightrect + width // 2), width)

currentSlider = None
class Slider():
    global currentSlider
    currentSlider = 0  # to set the cmyk-values correctly

    @classmethod
    def update(cls, mousePos, mouseDown, mouseClick, right=False, left=False):
        for obj in gc.get_objects():
            if isinstance(obj, Slider):
                if not mouseDown:
                    obj.clicked = False

                obj.updateInstance(mousePos, mouseDown, mouseClick)
                if currentSlider is None:
                    if obj.hover:
                        obj.marked = True
                        markedSlider = obj.index
                    else:
                        obj.marked = False
                else:
                    if obj.index == currentSlider or obj.clicked:
                        obj.marked = True
                        markedSlider = obj.index
                        if right:
                            obj.value += 1
                        if left:
                            obj.value -= 1
                    else:
                        obj.marked = False

    @classmethod
    def roundAllValues(cls):
        for obj in gc.get_objects():
            if isinstance(obj, Slider):
                obj.value = round(obj.value)

    @classmethod
    def showAll(cls):
        for obj in gc.get_objects():
            if isinstance(obj, Slider):
                obj.show()

    @classmethod
    def default(cls, attribute, val):
        '''attribute: '''
        for obj in gc.get_objects():
            if isinstance(obj, Slider):
                setattr(obj, attribute, val)

    def __init__(self,
                 minimum,
                 maximum,
                 surface,
                 value=None,
                 width=120,
                 height=30,
                 position=[0, 0],
                 lineColor=(128, 128, 128),
                 rectColor=(128, 128, 128),
                 outlineColor=(0, 0, 0),
                 outlineThickness=2,
                 lineThickness=8,
                 sliderThickness=14):
        if value is None or value > width or value < 0:
            value = width / 2
        self.position = position
        self.maximum = maximum
        self.minimum = minimum
        self.surface = surface
        self._value = value
        self.width = width
        self.height = height
        self.clicked = False
        self.hover = False
        self.index = 0
        self.lineColor = lineColor
        self.rectColor = rectColor
        self.outlineColor = outlineColor
        self.outlineThickness = outlineThickness
        self.lineThickness = lineThickness
        self.sliderThickness = sliderThickness
        self.marked = False

    def updateInstance(self, mousePos, mouseDown, mouseClick):
        if (((mousePos[0] <= self.width + self.position[0] + self.sliderThickness / 2 + 5 and mousePos[0] >= self.position[0] - (self.sliderThickness + 5)) and (mousePos[1] <= self.height + self.position[1] and mousePos[1] >= self.position[1]))):
            if mouseClick:
                global currentSlider
                currentSlider = self.index
                self.clicked = True

            self.hover = True
        else:
            self.hover = False
        if self.clicked:
            if mouseDown:
                if currentSlider == self.index:
                    if mousePos[0] > self.position[0] and mousePos[0] < self.position[0] + self.width:
                        self._value = mousePos[0] - self.position[0]
                    elif mousePos[0] >= self.position[0] + self.width:
                        self._value = self.width
                    elif mousePos[0] <= self.position[0]:
                        self._value = 0

    @property
    def value(self):
        return mapRange(self._value, 0, self.width, self.minimum, self.maximum)

    @value.setter
    def value(self, value):
        self._value = mapRange(value, self.minimum,
                               self.maximum, 0, self.width)
        if self._value > self.width:
            self._value = self.width
        elif self._value < 0:
            self._value = 0

    def show(self):
        if self.marked:
            rect(self.surface, self.outlineColor, (self.position[0] - self.sliderThickness // 2 - 2,
                                                   self.position[1] - 2, self.width + self.sliderThickness + 4, self.height + 4), self.outlineThickness)
        pygame.draw.line(self.surface, self.outlineColor, (self.position[0] - int((self.sliderThickness + self.outlineThickness) / 2.0000000001), self.position[1] + self.height / 2), (
            self.position[0] + (self.sliderThickness + self.outlineThickness) // 2 + self.width, self.position[1] + self.height / 2), self.lineThickness + self.outlineThickness)
        pygame.draw.line(self.surface, self.lineColor, (self.position[0] - int((self.sliderThickness - self.outlineThickness) / 2.0000000001), self.position[1] + self.height / 2), (
            self.position[0] + (self.sliderThickness - self.outlineThickness) // 2 + self.width, self.position[1] + self.height / 2), self.lineThickness - self.outlineThickness)
        pygame.draw.rect(self.surface, self.rectColor, (
            self.position[0] + self._value - self.sliderThickness // 2, self.position[1], self.sliderThickness, self.height))
        rect(self.surface, self.outlineColor, (self.position[0] + self._value - self.sliderThickness //
                                               2, self.position[1], self.sliderThickness, self.height), self.outlineThickness)
        pygame.draw.line(self.surface, self.outlineColor, (self.position[0] + self._value - 3, self.position[1] +
                                                           self.height / 2), (self.position[0] + self._value + 4, self.position[1] + self.height / 2), 2)
        pygame.draw.line(self.surface, self.outlineColor, (self.position[0] + self._value - 3, self.position[1] +
                                                           self.height / 2 + 4), (self.position[0] + self._value + 4, self.position[1] + self.height / 2 + 4), 2)
        pygame.draw.line(self.surface, self.outlineColor, (self.position[0] + self._value - 3, self.position[1] +
                                                           self.height / 2 - 4), (self.position[0] + self._value + 4, self.position[1] + self.height / 2 - 4), 2)
