import socket


class DiceData:

    def __init__(self, orientation, is_rolling):
        self.orientation = orientation
        self.is_rolling = is_rolling


class Dice:

    def __init__(self):
        self.idle_counter = 0
        self.values = [0, 0, 0]
        self.old_values = [0, 0, 0]
        self.delta = [0, 0, 0]

    def parse_content(self, c):
        array = c.split(" ")
        ax = float(array[1])
        ay = float(array[3])
        az = float(array[5])

        self.values = [ax, ay, az]

    def calculate_delta(self):
        delta = [0, 0, 0]

        for i in range(0, 2):
            delta[i] = -self.old_values[i] + self.values[i]

        self.delta = delta
        self.old_values = self.values

    def cube_idle_counter(self):
        if self.cube_moved():
            self.idle_counter = 0
        else:
            self.idle_counter += 1

        return self.idle_counter

    def cube_moved(self):
        result = False

        for i in range(0, 2):
            if (self.delta[i] < -0.05) | (self.delta[i] > 0.05):
                result = True

        return result

    def get_orientation(self):
        return [Dice.round_num(self.values[0]), Dice.round_num(self.values[1]), Dice.round_num(self.values[2])]

    def get_current_dice_roll_list(self):
        is_dice_rolling = self.idle_counter > 5

        return is_dice_rolling, self.get_orientation()

    def get_current_dice_roll_object(self):
        is_dice_rolling = self.idle_counter > 5

        return DiceData(self.get_orientation(), is_dice_rolling)

    @staticmethod
    def round_num(n):
        result = 0

        if n > 0.9:
            result = 1
        elif n < -0.9:
            result = -1

        return result


def run(ns):

    TCP_IP = '192.168.137.9'
    TCP_PORT = 80
    BUFFER_SIZE = 1024

    d = Dice()

    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 400, 300))        # socket keep alive
        s.connect((TCP_IP, TCP_PORT))

        data = s.recv(BUFFER_SIZE)

        d.parse_content(data)
        d.calculate_delta()
        d.cube_idle_counter()
        ns.dice_data = d.get_current_dice_roll_object()

        s.close()

