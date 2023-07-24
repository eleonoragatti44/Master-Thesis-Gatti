from parameters import *
from math import pi, cos, sin
from numpy import random as rnd
from vec2D import Vec2D
from individual import Individual, agent

#---------------------   SETUP   ---------------------

def SetupAgents(seed):
    """Setup agents with unit velocity vector and initial position depending on the symmetry."""
    global agent
    set_informed : int
    range_y = bottom_right.y - top_left.y
    # set seed for random variable
    if deterministic: rnd.seed(44)
    else: rnd.seed()

    for i in range(total_agents//2):
        if informed_group_size != 0:
            if (i / informed_group_size < number_of_cues): set_informed = i // informed_group_size
            else: set_informed = 100
        else: set_informed = 100    # means uninformed
        #agent[i].Setup(r_centre = RandomBoundedPoint(seed+i), direction = Vec2D(1.0, 0.0).rotate(rnd.uniform() * 360.0), max_turning_rate = max_turning_rate, speed = speed,
        #            zone_of_deflection = zod, zone_of_perception = zop, angular_error_sd = angular_error_sd, omega = set_omega, informed = set_informed)
        
        agent[i].Setup(r_centre = Vec2D(0, range_y/2), direction = Vec2D(1.0, -0.1), max_turning_rate = max_turning_rate, speed = speed,
                    zone_of_deflection = zod, zone_of_perception = zop, angular_error_sd = angular_error_sd, omega = set_omega, informed = set_informed)

        agent[i+total_agents//2].Setup(r_centre = Vec2D(0, range_y/2), direction = Vec2D(1.0, 0.1), max_turning_rate = max_turning_rate, speed = speed,
                    zone_of_deflection = zod, zone_of_perception = zop, angular_error_sd = angular_error_sd, omega = set_omega, informed = set_informed+1)

def RandomBoundedPoint(seed): 
    """Generate the initial position of the agent.
    In the symmetrical case it is around (arena_size/2, arena_size/2).
    In the astmmatrical case it is around (0, arena_size/2)."""
    range_x = bottom_right.x - top_left.x
    range_y = bottom_right.y - top_left.y
    random_x = rnd.uniform() * range_x / 100
    random_y = rnd.uniform() * range_y / 100
    if symmetric:
        random_x = random_x + range_x / 2.0 - range_x / 200.0
    random_y += range_y / 2.0 - range_y / 200.0
    return Vec2D(random_x, random_y)

def SetupEnvironmentSymmetric():
    """Setup symmetric environment."""
    global CS
    start = Vec2D(bottom_right.x / 2, bottom_right.y / 2)
    theta = overall_angle / (number_of_cues - 1)
    for i in range(number_of_cues):
        CS[i].Setup(start +
                    Vec2D(x = start_dist * cos(i * theta - overall_angle/2), y = start_dist * sin(i * theta - overall_angle/2)))

def SetupEnvironmentAsymmetric():
    """Setup asymmetric environment."""
    global CS
    start = Vec2D(0.0, arena_size / 2)
    theta = 0.0
    if (number_of_cues != 1): theta = max_angle / (number_of_cues - 1)
    for i in range(number_of_cues):
        CS[i].Setup(start +
                    Vec2D(x = start_dist * cos(i * theta - max_angle/2), y = start_dist * sin(i * theta - max_angle/2)))

def SetupSimulation(seed):
    """Setup the simulation."""
    global cue_reached
    cue_reached = -1
    if symmetric:
        SetupEnvironmentSymmetric()
    else:
        SetupEnvironmentAsymmetric()
    SetupAgents(seed)

#---------------------   CALCULATE AND MOVE   ---------------------

def MoveAgents(angular_thresh, beta):
    """Move agents according to social forces, feedback and personal preference."""
    global polarisation
    global cue_reached
    global agent
    global centroid
    global CS
    CalculateSocialForces(beta)
    CalculateGroupProperties()
    for i in range(number_of_cues):
        if (centroid.distanceTo(CS[i].centre) < dist_thresh * dist_thresh):
            cue_reached = i
    for i in range(total_agents):
        if (agent[i].informed != 100):
            agent[i].Feedback(CS[agent[i].informed].centre, angular_thresh, omega_inc, omega_dec, omega_max)
            agent[i].AddPersonalPreference(CS[agent[i].informed].centre)
        dev_angle = 2 * pi * rnd.normal(0.0, angular_error_sd)
        agent[i].Move(timestep_inc, dev_angle)

def CalculateSocialForces(beta):
    """Calculate social forces on all the individuals."""
    global agent
    global centroid
    dist : float
    temp_vector = Vec2D()
    # clear everything -> set everything to 0
    for i in range(total_agents):
        agent[i].zod_count = 0
        agent[i].zop_count = 0
        agent[i].total_zod.clear()
        agent[i].total_zop.clear()
        agent[i].total_allignament.clear()
        agent[i].attraction = False
    for i in range(total_agents):
        for j in range(i+1, total_agents):
            temp_vector = (agent[j].r_centre - agent[i].r_centre)
            # check to see if it is reasonable that you may be interacting
            if temp_vector.x * temp_vector.x <= zop and temp_vector.y * temp_vector.y <= zop:
                dist = agent[j].r_centre.distanceTo(agent[i].r_centre)
                temp_vector = temp_vector.normalise()
                if (dist <= zod):
                    agent[i].zod_count += 1
                    agent[j].zod_count += 1
                    # add repultion term
                    agent[i].total_zod -= temp_vector
                    agent[j].total_zod += temp_vector
                elif (dist <= zop):
                    agent[i].zop_count += 1
                    agent[j].zop_count += 1
                    # add attraction term
                    agent[i].total_zop += temp_vector
                    agent[i].total_allignament += agent[j].direction
                    agent[j].total_zop -= temp_vector
                    agent[j].total_allignament += agent[i].direction
    # now modify the direction according to the force
    for k in range(total_agents):
        if (agent[k].zod_count > 0):
            if (abs(agent[k].total_zod.x) < 1e-5 and abs(agent[k].total_zod.y) < 1e-5):
                agent[k].desired_direction = agent[k].direction
            else:
                agent[k].desired_direction = agent[k].total_zod.normalise()

        elif (agent[k].zop_count > 0):
            if(abs(agent[k].total_zop.x) < 1e-5 and abs(agent[k].total_zop.y) and abs(agent[k].total_allignament.x) and abs(agent[k].total_allignament.y) < 1e-5):
                agent[k].desired_direction = agent[k].direction
            else:
                agent[k].desired_direction = ( agent[k].total_zop + agent[k].total_allignament ).normalise() * beta
                #agent[k].attraction = True
        
def CalculateGroupProperties():
    """Calculate grouop properties about centroid and polarisation."""
    global centroid
    global polarisation
    global agent
    centroid.clear()
    polarisation.clear()
    for i in range(total_agents):
        centroid += agent[i].r_centre
        polarisation += (agent[i].direction.normalise())
    centroid /= total_agents
    polarisation /= total_agents

def SaveAgentsPosition(rep, time, name_datetime):
    """Save agents' positions at timestep = time."""
    global agent
    with open("../output/agents"+name_datetime+".txt", 'a') as fag:
        for i, ag in enumerate(agent):
            fag.write(f"{rep}\t{time}\t{i}\t{ag.r_centre.x}\t{ag.r_centre.y}\n")

def SaveAgentsDirection(rep, time, name_datetime):
    """Save agents' directions at timestep = time."""
    global agent
    with open("../output/dir"+name_datetime+".txt", 'a') as fag:
        for i, ag in enumerate(agent):
            fag.write(f"{rep}\t{time}\t{i}\t{ag.direction.x}\t{ag.direction.y}\n")

#---------------------   GROUP TOGETHER   ---------------------

def GroupTogether():
    global agent
    EquivalenceClasses()
    group_size = 0
    equivalence_class = 0
    equivalence_class = agent[0].equivalence_class
    for i in range(total_agents):
        if(agent[i].equivalence_class == equivalence_class): group_size += 1
    if(group_size == total_agents):
        return True
    else:
        return False

def Equivalent(ag1, ag2):
    largest_zone = ag1.zone_of_deflection if (ag1.zone_of_deflection > ag1.zone_of_perception) else ag1.zone_of_perception
    if(ag1.r_centre.distanceTo(ag2.r_centre) < largest_zone):
        return True
    else:
        return False

def EquivalenceClasses():
    global agent
    nf = [int]*total_agents
    for j in range(total_agents):
        nf[j] = j
        for k in range(j):
            nf[k] = nf[nf[k]]
            if(Equivalent(agent[j], agent[k])): nf[nf[nf[k]]] = j
    for j in range(total_agents):
      nf[j] = nf[nf[j]]
    for j in range(total_agents):
        agent[j].equivalence_class = nf[j]


#---------------------##########---------------------
#---------------------   MAIN   ---------------------
#---------------------##########---------------------

def task(i, name_datetime, angular_thresh, beta, num_replicates):
    global agent
    global centroid
    result = True
    print(i)
    SetupSimulation(i)
    with open(f"../output/centroid"+name_datetime+".txt", 'a') as f:
        #SaveAgentsDirection(i, -1, name_datetime) 
        for j in range(num_timesteps):
            MoveAgents(angular_thresh, beta)
            if j%50 == 0 and cue_reached==-1:
                result = GroupTogether()
                f.write(f"{i}\t{j}\t{result}\t{centroid.x:.20f}\t{centroid.y:.20f}\t{cue_reached}\n")
            #SaveAgentsPosition(i, j, name_datetime)  
            #SaveAgentsDirection(i, j, name_datetime)    
            if cue_reached!=-1 or not result:
                f.write(f"{i}\t{j}\t{result}\t{centroid.x:.20f}\t{centroid.y:.20f}\t{cue_reached}\n")
                break
        if i == num_replicates - 1:
            # save target position just at the end
            with open("../output/targets"+name_datetime+".txt", 'w') as fc:
                fc.write(f"id\tx\ty\n")
                for i in range(number_of_cues): 
                    fc.write(f"{i}\t{CS[i].centre.x}\t{CS[i].centre.y}\n")