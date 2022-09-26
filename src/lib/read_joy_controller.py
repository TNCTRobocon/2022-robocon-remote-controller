from pygame import joystick, event
import pygame

from typing import List

class ReadJoyController:

    def __init__(self):
        pygame.init()
        joystick.init()
        if joystick.get_count() <= 0:
            exit('Joycontroller not found!!')
        self.js = joystick.Joystick(0)
        self.js.init()
        self.debug_pad_data = 0
        print("joystick: " + str(self.js.get_numaxes()) + "\n")
        print("button: " + str(self.js.get_numbuttons()) + "\n")
        print("hat: " + str(self.js.get_numhats()) + "\n")
        self.get_joystick()

    def get_joystick_data(self):
        self.get_joystick()
        return self.pad_data_joystick, self.pad_data_button

    def check_event(self) -> bool:
        return bool(event.get())

    def axis_ftoi(self, val):
        val = round(val, 2)
        in_min = -1
        in_max = 1
        out_min = 0
        out_max = 255
        return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def get_debug(self):
        if event.get():
            return [
                round(self.js.get_axis(0),2),   #lx lx
                round(self.js.get_axis(1),2),   #ly ly
                round(self.js.get_axis(2),2),   #rx lt
                round(self.js.get_axis(3),2),   #ry rx
                round(self.js.get_axis(4),2),   #lt ry
                round(self.js.get_axis(5),2),   #rt rt
                self.js.get_hat(0)[0],
                self.js.get_hat(0)[1],
                self.js.get_button(0),
                self.js.get_button(1),
                self.js.get_button(2),
                self.js.get_button(3),
                self.js.get_button(4),
                self.js.get_button(5),
                self.js.get_button(6),
                self.js.get_button(7),
                self.js.get_button(8),
                self.js.get_button(9),
                self.js.get_button(10)
            ]

    def get_joystick(self) -> None:
        self.pad_data_joystick:List[int] = [
            self.axis_ftoi(self.js.get_axis(0)),    #joylx
            -self.axis_ftoi(self.js.get_axis(1)),   #joyly
            self.axis_ftoi(self.js.get_axis(3)),    #joyrx
            -self.axis_ftoi(self.js.get_axis(4)),   #joyry
            self.axis_ftoi(self.js.get_axis(2)),    #lt
            self.axis_ftoi(self.js.get_axis(5))     #rt
        ]
        self.pad_data_button:List[bool] = [
            1 if self.js.get_hat(0)[0] > 0 else 0,  #up
            1 if self.js.get_hat(0)[0] < 0 else 0,  #down
            1 if self.js.get_hat(0)[1] > 0 else 0,  #right
            1 if self.js.get_hat(0)[1] < 0 else 0,  #left
            self.js.get_button(0),  #a
            self.js.get_button(1),  #b
            self.js.get_button(2),  #x
            self.js.get_button(3),  #y
            self.js.get_button(4),  #l
            self.js.get_button(5),  #r
            self.js.get_button(6),  #back
            self.js.get_button(7),  #start
            self.js.get_button(8),  #joyl
            self.js.get_button(9),  #joyr
            self.js.get_button(10)  #logi
        ]
        return
