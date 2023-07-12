import numpy as np
import matplotlib.pyplot as plt

################################################################################
#-----------------------------TOY MODEL - 2 TARGETS-----------------------------
################################################################################

# TOOLS

def delta_dirac(x):
    if x == 0:
        return 1
    else:
        return 0

def theta_heav(x):
    if x < 0:
        return 0
    else:
        return 1

# ODEs
def f_2D(x, t, params):
    '''Computes the derivative of x at t.'''
    theta1, theta2, J1, J2 = x
    alpha, beta, J, Jmax, theta0, omega = params
    return [
            -J*np.sin(theta1-theta2) - J1*np.sin(theta1-omega),   # Theta 1

            J*np.sin(theta1-theta2) - J2*np.sin(theta2+omega),    # Theta 2

            alpha*(Jmax-J1) * theta_heav(theta0 - abs(theta1-omega)) - beta*J1*(theta_heav(abs(theta1-omega) - theta0)), # J1
            
            alpha*(Jmax-J2) * theta_heav(theta0 - abs(theta2+omega)) - beta*J2*(theta_heav(abs(theta2+omega) - theta0))  # J2                                                        
           ]

# PLOT
def plot_results(res):
    fig, ax = plt.subplots(2, 1, sharex=True, figsize=(8, 6))
    ax[0].plot(res.t, np.degrees(res.y[0]), label=r'$\theta_1$', alpha=.8)
    ax[0].plot(res.t, np.degrees(res.y[1]), label=r'$\theta_2$', alpha=.8)
    ax[0].set_ylabel('Angle (deg)')
    ax[0].set_ylim(-180, 180)
    ax[0].legend()
    ax[1].plot(res.t, res.y[2], label=r'$J_1$')
    ax[1].plot(res.t, res.y[3], label=r'$J_2$')
    ax[1].set_xlabel('Time (s)')
    ax[1].set_ylabel('Feedback')
    #ax[1].set_ylim(-0.1, 0.5)
    ax[1].legend(loc=3)
    plt.suptitle('Angle and feedback over time')
    plt.show()

def plot_traj(res):
    fig, ax = plt.subplots(1, figsize=(8, 4))
    ax.plot(res.t, np.cumsum(np.cos(res.y[0]+np.pi/2)+np.cos(res.y[1]+np.pi/2)))
    ax.set_xlabel('Time')
    ax.set_ylabel('Position')
    plt.suptitle('Trajectory over time')
    plt.show()


################################################################################
#-----------------------------TOY MODEL - 2 TARGETS-----------------------------
################################################################################

# TOOLS

def sign(x):
    '''Compute the sign of x.'''
    if x >= 0:
        return 1
    elif x < 0:
        return -1

def delta_inv(x):
    return 0 if abs(x) < 1e-2 else 1

def omega(x, y, xt, yt):
        '''Compute the angular distance of the target (with respect of horizontal axis passing for (x, y) point).'''
        return np.arccos((xt-x)/np.sqrt((xt-x)**2 + (yt-y)**2))

# ODEs

def f_XY(var, t, params):
    '''Computes the derivative of x at t.'''
    # x, y, theta1, theta2, J1, J2 = var
    x, y, theta1, theta2, J1, J2 = var
    # the upper target is defined by (xt, yt)
    # then the lower target is defined by same x but opposite y
    alpha, beta, Ja, Jmax, theta0, xt, yt = params

    return [(np.cos(theta1) + np.cos(theta2)) * delta_inv(round(abs(x-xt)/xt,2)), #* delta_inv(round(abs(x-xt)/xt,2) + round(abs(y-yt))/yt) * delta_inv(round(abs(x-xt)/xt,2) + round(abs(y+yt))/yt), # x

            (np.sin(theta1) + np.sin(theta2)) * delta_inv(round(abs(x-xt)/xt,2)), #* delta_inv(round(abs(x-xt)/xt,2) + round(abs(y-yt))/yt) * delta_inv(round(abs(x-xt)/xt,2) + round(abs(y+yt))/yt), # y 

            -Ja*np.sin(theta1-theta2) - J1*np.sin(theta1-sign(yt-y)*omega(x, y, xt, yt)),   # Theta 1

            Ja*np.sin(theta1-theta2)- J2*np.sin(theta2-sign(-yt-y)*omega(x, y, xt, -yt)),     # Theta 2

            alpha*(Jmax-J1)*theta_heav(theta0-abs(theta1-sign(yt-y)*omega(x, y, xt, yt)))  - beta*J1*theta_heav(abs(theta1-sign(yt-y)*omega(x, y, xt, yt)) - theta0), # J1
            
            alpha*(Jmax-J2)*theta_heav(theta0-abs(theta2-sign(-yt-y)*omega(x, y, xt, -yt)))   - beta*J2*theta_heav(abs(theta2-sign(-yt-y)*omega(x, y, xt, -yt)) - theta0) # J2
            ]


def f_XY_4eq(var, t, params):
    '''Computes the derivative of x at t.'''
    # x, y, theta1, theta2, J1, J2 = var
    x, y, theta1, theta2 = var
    # the upper target is defined by (xt, yt)
    # then the lower target is defined by same x but opposite y
    Ja, Jmax, theta0, xt, yt = params

    return [(np.cos(theta1) + np.cos(theta2)) * delta_inv(round(abs(x-xt)/xt,2)), #* delta_inv(round(abs(x-xt)/xt,2) + round(abs(y-yt))/yt) * delta_inv(round(abs(x-xt)/xt,2) + round(abs(y+yt))/yt), # x

            (np.sin(theta1) + np.sin(theta2)) * delta_inv(round(abs(x-xt)/xt,2)), #* delta_inv(round(abs(x-xt)/xt,2) + round(abs(y-yt))/yt) * delta_inv(round(abs(x-xt)/xt,2) + round(abs(y+yt))/yt), # y 

            -Ja*np.sin(theta1-theta2) - Jmax*theta_heav(theta0-abs(theta1-sign(yt-y)*omega(x, y, xt, yt)))*np.sin(theta1-sign(yt-y)*omega(x, y, xt, yt)),   # Theta 1

            Ja*np.sin(theta1-theta2)- Jmax*theta_heav(theta0-abs(theta2-sign(-yt-y)*omega(x, y, xt, -yt)))*np.sin(theta2-sign(-yt-y)*omega(x, y, xt, -yt))     # Theta 2
            ]

# PLOT

# plotting trajectory on x-y plane
def plot_traj(res, params):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(res.y[0], res.y[1], alpha=.8, marker='.', c='black')
    ax.scatter(params[5], params[6], c='r')
    ax.scatter(params[5], -params[6], c='r')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Trajectory')
    plt.show()

# plotting trajectory on x-y plane given ax as input
def plot_traj_ax(res, params, ax, len):
    ax.plot(res.y[0], res.y[1], alpha=1/len, c='black')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Trajectory')
    #return ax

# plotting x and y over time
def plot_xy(res):
    fig, ax = plt.subplots(2, 1, sharex=True, figsize=(8, 6))
    ax[0].scatter(res.t, res.y[0], alpha=.8)
    ax[1].scatter(res.t, res.y[1], alpha=.8)
    ax[0].set_ylabel('x')
    ax[1].set_xlabel('Time (s)')
    ax[1].set_ylabel('y')
    #ax.set_title('Trajectory')
    plt.show()

# plotting thetas and Js over time
def plot_thetasJs(res):
    fig, ax = plt.subplots(2, 1, sharex=True, figsize=(8, 6))
    ax[0].plot(res.t, np.degrees(res.y[2]), label=r'$\theta_1$', alpha=.8)
    ax[0].plot(res.t, np.degrees(res.y[3]), label=r'$\theta_2$', alpha=.8)
    ax[0].set_ylabel('Angle (deg)')
    #ax[0].set_ylim(-180, 180)
    ax[0].legend()
    ax[1].plot(res.t, res.y[4], label=r'$J_1$')
    ax[1].plot(res.t, res.y[5], label=r'$J_2$')
    ax[1].set_xlabel('Time (s)')
    ax[1].set_ylabel('Feedback')
    #ax[1].set_ylim(-0.1, 0.5)
    ax[1].legend(loc=3)
    plt.suptitle('Angle and feedback over time')
    plt.show()

# plotting thetas and Js over time
def plot_thetas(res):
    fig, ax = plt.subplots(1, 1, sharex=True, figsize=(8, 6))
    ax.plot(res.t, np.degrees(res.y[2]), label=r'$\theta_1$', alpha=.8)
    ax.plot(res.t, np.degrees(res.y[3]), label=r'$\theta_2$', alpha=.8)
    ax.set_ylabel('Angle (deg)')
    #ax[0].set_ylim(-180, 180)
    ax.legend()
    
    ax.set_xlabel('Time (s)')

    plt.suptitle('Angle over time')
    plt.show()

def plot_omega(res, xt, yt):
    fig, ax = plt.subplots(1, 1, sharex=True, figsize=(8, 6))
    ax.plot(res.t, np.degrees(omega(res.y[0], res.y[1], xt, yt)), label=r'$\omega$', alpha=.8)
    ax.set_ylabel('Angle (deg)')
    #ax[0].set_ylim(-180, 180)
    ax.legend()
    
    ax.set_xlabel('Time (s)')

    plt.suptitle('Omega over time')
    plt.show()