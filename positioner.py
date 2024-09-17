# TODO: add state and logging for Positioner class
# TODO: add Positioner class, should contain:
# center of positioner
# theta range approx 390
# phi range approx 190
# theta_max is hard stop
# phi_max is hard stop
# current position
# counterclockwise is positive

from test_gen import fit_circle
class Positioner:
    def __init__(self, center, theta_arm_length, phi_arm_length, theta_max, phi_max, current_x, current_y,
                 current_theta, current_phi):
        self.theta_arm_length = theta_arm_length
        self.phi_arm_length = phi_arm_length
        self.center = center
        self.theta_max = theta_max
        self.phi_max = phi_max
        self.current_x = current_x
        self.current_y = current_y
        self.current_theta = current_theta
        self.current_phi = current_phi
        self.moves = []
        # movement speeds?

    def compute_center(self):
        # move theta arm in circle and run a circle fitter
        pass

    def compute_theta_arm_length(self):
        # get value from computed center
        pass

    def compute_phi_arm_length(self):
        # move phi arm in a circle and run a circle fitter
        pass

    # add a move to self.moves every time a move is made
    def add_move(self, x, y):
        pass

    # export self.moves to a JSON file?
    def log(self):
        pass

    # draw out all moves in self.moves sequentially
    def visualize_moves(self):
        pass
