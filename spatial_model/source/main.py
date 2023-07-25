from vec2D import Vec2D
from individual import Individual, agent
from cue import Cue
from parameters import *
from utils import *

from numpy import random as rnd
import numpy as np
from math import pi, cos, sin
from datetime import datetime
from multiprocessing import Pool

import sys
import time
import click

#---------------------##########---------------------
#---------------------   MAIN   ---------------------
#---------------------##########---------------------

@click.group()
def cli():
    pass

@click.command("run")
@click.option("--name_datetime", type=str, default=datetime.now().strftime("%Y%m%d-%H%M%S"), help="Name for output files")
@click.option("--angular_thresh", type=float, default=20.0*pi/180, help="Value of angular threshold in radiant")
@click.option("--beta", type=float, default=1, help="Value of beta")
@click.option("--num_replicates", type=int, default=100, help="Number of replicates")

def run(name_datetime, angular_thresh, beta, num_replicates):
    global cue_reached
    global centroid
    global agent

    # output file for centroid positions
    with open(f"../output/centroid"+name_datetime+".txt", 'w') as f:
        f.write(f"replicate\ttime\tresult\tx\ty\tcue_reached\n")
    angular_thresh = np.radians(angular_thresh)
    # iterable for the multiprocessing pools
    items = [(i, name_datetime, angular_thresh, beta, num_replicates) for i in range(num_replicates)]
    # multiprocessing run over num_replicates
    with Pool() as pool:
        pool.starmap(task, items)

    # save simulation's parameters
    with open("../output/parameters"+name_datetime+".txt", 'w') as fp:
        fp.write(f"total_agents\t{total_agents}\n")
        fp.write(f"number_of_cues\t{number_of_cues}\n")
        fp.write(f"informed_group_size\t{informed_group_size}\n")
        fp.write(f"num_replicates\t{num_replicates}\n")
        fp.write(f"num_timesteps\t{num_timesteps}\n")
        fp.write(f"time step_inc\t{timestep_inc}\n")
        fp.write(f"angular_error_sd\t{angular_error_sd}\n")
        fp.write(f"max_turning_rate\t{max_turning_rate}\n")
        fp.write(f"speed\t{speed}\n")
        fp.write(f"beta\t{beta}\n")
        fp.write(f"angular_thresh\t{angular_thresh}\n")
        fp.write(f"set_omega\t{set_omega}\n")
        fp.write(f"omega_inc\t{omega_inc}\n")
        fp.write(f"omega_dec\t{omega_dec}\n")
        fp.write(f"omega_max\t{omega_max}\n")
        fp.write(f"max_angle\t{max_angle}\n")

cli.add_command(run)

if __name__ == "__main__":
    cli()
    



# add header to agents' file
# with open("../output/agents"+name_datetime+".txt", 'r+') as file: 
#     file_data = file.read() 
#     file.seek(0, 0) 
#     file.write("replicate\ttime\tid\tx\ty\n"+file_data) 


# add header to dir' file
# with open("../output/dir"+name_datetime+".txt", 'r+') as file: 
#     file_data = file.read() 
#     file.seek(0, 0) 
#     file.write("replicate\ttime\tid\tdir_x\tdir_y\n"+file_data) 