import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from matplotlib.animation import FuncAnimation

# graphs set-up
sns.set(color_codes=True)

# variables for simulation
dmu = 0.000001  # small change in mu
dsigma = 0.001  # small change in sigma
dt = 1  # change in time = 1 day
startvalue = 6000  # start value value of FTSE 100 projections
endtime = 1.0  # time = 1 year
simsteps = 252  # number of steps in the simulation, trading days
numberoftrials = 100  # number of trials in each Monte Carlo projection
np.random.seed(123)  # setting the random number seed
mus = np.linspace(0.02, 0.12, 6)  # space for the mus
sigmas = np.linspace(0.04, 0.2, 5)  # space for the sigmas
m2, s2 = np.meshgrid(mus, sigmas)  # set-up of grid of values of sigma and mus to search over
coords = np.array((m2.ravel(), s2.ravel())).T  # turns grid into mu/sigm coordinates
major_ticks = np.arange(0, 0.15, 0.02)
ymajorticks = np.arange(0, 0.21, 0.04)
finalmean = 0.05  # proxy target for the mean
finalsd = 0.18  # proxy target for the standard deviation

# Monte carlo function


def montecarlo(timezerovalue, trialmu, trialsigma, theendtime, numberofsteps, numberoftrialsinproj):
    deltat = float(theendtime) / simsteps
    paths = np.zeros((numberofsteps + 1, numberoftrialsinproj), np.float64)
    paths[0] = timezerovalue
    for t in range(1, numberofsteps + 1):
        rand = np.random.standard_normal(numberoftrialsinproj)
        paths[t] = paths[t - 1] * np.exp((trialmu - 0.5 * trialsigma ** 2) *
                                         deltat + trialsigma * np.sqrt(deltat) * rand)
    return paths


# A basic optimiser function, nothing rigorous and no weighting


def optimiser(mean, standdev):
    optimal = (mean / startvalue - finalmean) ** 2 + (finalsd - standdev / mean) ** 2
    return optimal


# Set-up of subplots
fig = plt.figure(constrained_layout=True, figsize=(15, 10))
grid = gridspec.GridSpec(ncols=9, nrows=3, figure=fig)
ax1 = fig.add_subplot(grid[0:2, 0:2])
ax2 = fig.add_subplot(grid[0:3, 2:7])
ax3 = fig.add_subplot(grid[0:3, 7:9])
ax4 = fig.add_subplot(grid[2:3, 0:2], projection='3d')

# Define titles of subplots
ax1.set_title('Parameters')
ax2.set_title('Simulations')
ax3.set_title('Distribution')
ax4.set_title('Optimiser')

# Set background colours for subplots
ax1.set_facecolor('azure')
ax3.set_facecolor('lavenderblush')
ax4.set_facecolor('greenyellow')

# Set-up axes labels
ax1.set_xlabel('mu')
ax1.set_ylabel('sigma')
ax2.set_xlabel('Time')
ax2.set_ylabel('FTSE 100')
ax3.set_xlabel('Density')
ax3.set_ylabel('Daily return')
ax4.set_xlabel('mu')
ax4.set_ylabel('sigma')
ax4.set_zlabel('Value')
ax4.tick_params(axis='z', which='both', bottom=False, top=False)
ax1.set_xticks(major_ticks)
ax1.set_yticks(ymajorticks)
ax1.grid(color='black')
ax3.grid(color='black')
ax4.grid(color='black')
ax1.plot(m2, s2, marker='.', color='k', linestyle='none')


# A function to calculate and plot the kernel density


def kde(returns):
    sns.kdeplot(y=returns, shade=True, ax=ax3)
    ax3.tick_params(axis='x', which='both', bottom=False, top=False)


# The main function for updating the animation and it is called later when the animation is created


def updateanim(i):
    global startvalue, endtime, simsteps, coords
    simresults = montecarlo(startvalue, coords[i][0], coords[i][1], endtime, simsteps, numberoftrials)
    ax2.clear()
    ax3.clear()
    ax3.grid(color='black')
    ax2.set_title('Simulations')
    ax3.set_title('Distribution')
    ax2.set_xlim(0, 250)
    ax2.set_ylim(4000, 10000)
    ax3.set_xlim(0, 0.002)
    ax3.set_ylim(4000, 10000)
    ax4.set_ylim(0, 0.21)
    ax4.set_xlim(0, 0.15)
    ax4.set_zlim(0, 1.5)
    ax2.set_xlabel('Time')
    ax2.set_ylabel('FTSE 100')
    ax3.set_xlabel('Density')
    ax1.scatter(coords[i][0], coords[i][1], s=100, color='red')  # mu/sigma lattice
    ax2.plot(simresults)  # displays the Monte Carlo output for a given mu and sigma
    kde(simresults[-1])  # displays the output of the a simulation as a distribution plot
    sdfinal = np.std(simresults[-1])  # sd of the trials for a given mu/sigma
    mufinal = np.mean(simresults[-1])  # mean of the trials for a given mu/sigma
    finalop = optimiser(mufinal, sdfinal)  # value of the optimiser
    ax1.scatter(coords[i][0], coords[i][1], s=100, color='gold')  # colours in grid point in mu/sigma space
    ax4.scatter3D(coords[i][0], coords[i][1], finalop)  # plots the value of the optimiser


anim = FuncAnimation(fig, updateanim, interval=500)
anim.save('animationoutput.mp4')

grid.tight_layout(fig)
plt.show()
