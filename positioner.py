# TODO: add state and logging for Positioner class
# TODO: add Positioner class, should contain:
# center of positioner
# theta range approx 390
# phi range approx 190
# theta_max is hard stop
# phi_max is hard stop
# current position
# counterclockwise is positive
class Positioner:
    def __init__(self, center, arm_length, theta_max, phi_max, current_x, current_y, current_theta, current_phi):
        self.arm_length = arm_length
        self.center = center
        self.theta_max = theta_max
        self.phi_max = phi_max
        self.current_x = current_x
        self.current_y = current_y
        self.current_theta = current_theta
        self.current_phi = current_phi
        self.moves = []

    def add_move(self, x, y):
        pass

    def log(self):
        pass