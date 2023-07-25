from vec2D import Vec2D
#from individual import Individual
from cue import Cue
from math import pi
from datetime import datetime
import sys

# Define arena's corner
arena_size = 1000
top_left = Vec2D(0.0, 0.0)
bottom_right = Vec2D(arena_size, arena_size)

# Define simulation's parameters
#num_replicates = 100
num_timesteps = 10000
cue_reached = -1

# Define system's parameters
number_of_cues : int = 2
timestep_inc = 0.1
total_agents = 60
informed_group_size = 30
angular_error_sd = 0.0
max_turning_rate = 2    # radiants
zod = 1
zop = 36.0

speed = 1.0
set_omega = 0.3

omega_inc = 0.012
omega_dec = 0.0008
omega_max = 0.4
dist_thresh = 10.0
start_dist = 450
overall_angle = 0.174533 #pi/4    # used for the symmetric case ('overall_angle' is split into 'number_of_cues' equal angles)
max_angle = pi/3        # used for the asymmetric case ('max_angle' is split into 'number_of_cues' - 1 equal angles)

#agent = [Individual() for i in range(total_agents)]
CS = [Cue() for i in range(number_of_cues)]
centroid = Vec2D()
polarisation = Vec2D()
#name_datetime = str(sys.argv[1]) if len(sys.argv) > 1 else datetime.now().strftime("%Y%m%d-%H%M%S")
#name_datetime : str

rep_done = False
time_up = False
symmetric = False
deterministic = False
positive_feedback = True

