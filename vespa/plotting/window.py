from graphics import *
from collections import deque
import threading
import time


class Window:
    """
    Wrapper for graphics object, window crashes when shapes are accessed from
    more than one thread
    """
    def __init__(self, name, winx, winy):
        self.updates = deque(maxlen=100)
        self.shapes = {}
        self.alive = True
        self.last_mouse_pos = None
        self.runner = threading.Thread(target=self.run, args=[name, winx, winy])
        self.runner.start()

    def run(self, name, winx, winy):
        self._create_window(name, winx, winy)
        while self.alive:
            self._find_last_mouse_pos()
            self._apply_updates()
            time.sleep(.1)

    def _create_window(self, name, winx, winy):
        self.win = GraphWin(name, winx, winy)

    def add_circle(self, _id, x, y, rad):
        funcdef = {'func': self._add_circle, 'args': [_id, x, y, rad]}
        self.updates.append(funcdef)

    def _add_circle(self, _id, x, y, rad):
        if _id not in self.shapes:
            self.shapes[_id] = {'ref': Circle(Point(x, y), rad),
                                'pos': (x, y),
                                'rad': rad}
            self.shapes[_id]['ref'].draw(self.win)
        else:
            print 'shape already in window'

    def move_shape(self, _id, x, y):
        """
        moves shape relative to its current pos
        """
        funcdef = {'func': self._move_shape, 'args': [_id, x, y]}
        self.updates.append(funcdef)

    def _move_shape(self, _id, x, y):
        self.shapes[_id]['ref'].move(x, y)
        curx, cury = self.shapes[_id]['pos']
        self.shapes[_id]['pos'] = (curx + x, cury + y)

    def set_shape_pos(self, _id, absx, absy):
        """
        sets the absolute position of the object
        """
        funcdef = {'func': self._set_shape_pos, 'args': [_id, absx, absy]}
        self.updates.append(funcdef)

    def _set_shape_pos(self, _id, absx, absy):
        curx, cury = self.shapes[_id]['pos']
        self.shapes[_id]['ref'].move(absx - curx, absy - cury)
        self.shapes[_id]['pos'] = (absx, absy)

    def get_last_mouse_pos(self):
        return self.last_mouse_pos

    def get_pos(self, _id):
        return self.shapes[_id]['pos']

    def _find_last_mouse_pos(self):
        pos = self.win.checkMouse()
        if pos is not None:
            self.last_mouse_pos = (pos.x, pos.y)

    def _apply_updates(self):
        if len(self.updates) > 0:
            update = self.updates.popleft()
            update['func'](*update['args'])

    def shutdown(self):
        self.alive = False

    def __del__(self):
        self.win.close()

if __name__ == '__main__':
    w = Window('name', 400, 300)
    w.add_circle(1, 100, 100, 10)

    def set1():
        while w.alive:
            w.set_shape_pos(1, 100, 100)
            time.sleep(.7)

    def set2():
        while w.alive:
            w.set_shape_pos(1, 200, 200)
            time.sleep(.95)

    def set3():
        while w.alive:
            print w.get_last_mouse_pos()
            time.sleep(.8)

    a = threading.Thread(target=set1)
    a.start()
    b = threading.Thread(target=set2)
    b.start()
    c = threading.Thread(target=set3)
    c.start()

    raw_input()
    w.shutdown()