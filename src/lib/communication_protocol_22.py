#   96start num
#   88start num
#   80A B X Y RB LB - -
#   72up down right left start back logi -
#   64joy rx
#   56joy ry
#   48joy lx
#   40joy ly
#   32rt
#   24lt
#   16emargency
#    8check sum

#   0joylx 1joyly 2joyrx 3joyry 4joylt 5joyrt
#   0up 1down 2right 3left 4a 5b 6x 7y 8l 9r 10back 11start 12joyl 13joyr 14logi

from typing import Final, List

class CommunicationProtocol22:

    STARTNUM1 = 0xAD
    STARTNUM2 = 0xBC
    STARTNUM:Final[int] = STARTNUM1 << 8 | STARTNUM2

    def __init__(self):
        self.emargency_b11 = 0
        self.checksum_created = False
        self.checksum_tf = False

    def __set_data(self, joystick_data, button_data) -> None:
        self.btn1_b3 = button_data[4] << 7 | button_data[5] << 6 | button_data[6] << 5 | button_data[7] << 4 | button_data[9] << 3 | button_data[8] << 2
        self.btn2_b4 = button_data[0] << 7 | button_data[1] << 6 | button_data[2] << 5 | button_data[3] << 4 | button_data[10] << 3 | button_data[11] << 2
        self.joyrx_b5 = joystick_data[2] & 0xFF
        self.joyry_b6 = joystick_data[3] & 0xFF
        self.joylx_b7 = joystick_data[0] & 0xFF
        self.joyly_b8 = joystick_data[1] & 0xFF
        self.rt_b9 = joystick_data[5]    & 0xFF
        self.lt_b10 = joystick_data[4]   & 0xFF
        return

    def generate_checksum(self) -> None:
        self.checksum_b12 = (self.btn1_b3 + self.btn2_b4 + self.joyrx_b5 + self.joyry_b6 + self.joylx_b7 + self.joyry_b6 + self.rt_b9 + self.lt_b10 + self.emargency_b11) % 100
        self.checksum_created = True
        return

    def check_checksum(self) -> bool:
        if self.checksum_b12 == (self.btn1_b3 + self.btn2_b4 + self.joyrx_b5 + self.joyry_b6 + self.joylx_b7 + self.joyry_b6 + self.rt_b9 + self.lt_b10 + self.emargency_b11) % 100:
            self.checksum_tf = True
        else:
            self.checksum_tf = False
        return self.checksum_tf

    def encode(self, joystick, button) -> int:
        self.__set_data(joystick, button)
        self.generate_checksum()
        send_data:int = self.STARTNUM1 << 88 | self.STARTNUM2 << 80 | self.btn1_b3 << 72 | self.btn2_b4 << 64 | self.joyrx_b5 << 56 | self.joyry_b6 << 48 | self.joylx_b7 << 40 | self.joyly_b8 << 32 | self.rt_b9 << 24 | self.lt_b10 << 16 | self.emargency_b11 << 8 | self.checksum_b12
        print('send_data : ' + hex(send_data) + '\n')
        return send_data

    def decode(self, responce_data):
        self.btn1_b3 = responce_data & 0xFF << 72
        self.btn2_b4 = responce_data & 0xFF << 64
        self.joyrx_b5 = responce_data & 0xFF << 56
        self.joyry_b6 = responce_data & 0xFF << 48
        self.joylx_b7 = responce_data & 0xFF << 40
        self.joyly_b8 = responce_data & 0xFF << 32
        self.rt_b9 = responce_data & 0xFF << 24
        self.lt_b10 = responce_data & 0xFF << 16
        self.emargency_b11 = responce_data & 0xFF << 8
        self.checksum_b12 = responce_data & 0xFF
        print(int(self.joyrx_b5))
        print(' ')
        print(int(self.joyry_b6))
        print(' ')
        print(int(self.joylx_b7))
        print(' ')
        print(int(self.joyly_b8))
        print(' ')
        print(int(self.rt_b9))
        print(' ')
        print(int(self.lt_b10))
        print(' ')
        print(self.btn1_b3)
        print(' ')
        print(self.btn2_b4)
        return self.check_checksum()
