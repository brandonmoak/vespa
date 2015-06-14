from graphics import *
import time


class Window:
    def __init__(self, name, winx, winy):
        self.win = GraphWin(name, winx, winy)
        self.shapes = {}
        self.alive = True
        self.last_mouse_pos = None

    def add_circle(self, _id, x, y, rad):
        self.shapes[_id] = {'ref': Circle(Point(x, y), rad),
                            'pos': (x, y),
                            'rad': rad}
        self.shapes[_id]['ref'].draw(self.win)

    def set_circle_param(self, _id, x, y, rad):
        pass

    def get_pos(self, _id):
        return self.shapes[_id]['pos']

    def move_shape(self, _id, x, y):
        """
        moves shape relative to its current pos
        """
        self.shapes[_id]['ref'].move(x, y)
        curx, cury = self.shapes[_id]['pos']
        self.shapes[_id]['pos'] = (curx + x, cury + y)

    def set_shape_pos(self, _id, absx, absy):
        """
        sets the absolute position of the object
        """
        curx, cury = self.shapes[_id]['pos']
        self.shapes[_id]['ref'].move(absx - curx, absy - cury)
        self.shapes[_id]['pos'] = (absx, absy)

    def get_last_mouse_pos(self):
        pos = self.win.checkMouse()
        if pos is not None:
            self.last_mouse_pos = (pos.x, pos.y)
        return self.last_mouse_pos

    def redraw(self):
        for _id in self.shapes:
            self.shapes[_id]['ref'].draw(self.win)

    def __del__(self):
        self.win.close()
