### GRAPHS
import rosbag
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
import numpy as np


### GRAPHS
### animated position plot **IS NOT CALLED, implemented in main method**
def animatedPositionPlot(ax, fig, husky_x_pos, husky_y_pos, human_x_pos, human_y_pos, minX, minY, maxX, maxY, times, human_times):

    husky_line = ax[0,0].plot(husky_x_pos[0], husky_y_pos[0], label=f"Husky")[0]
    human_line = ax[0,0].plot(human_x_pos[0], human_y_pos[0], label=f"Human")[0]
    ax[0,0].set(xlim=[minX-1, 1.1*maxX], ylim=[minY-1,1.1*maxY], xlabel='x-position', ylabel='y-position', title = 'Animated Position Plot')
    ax[0,0].legend()

    def update(frame):
        # update the line plot:
        husky_line.set_xdata(husky_x_pos[:frame])
        husky_line.set_ydata(husky_y_pos[:frame])
        #
        for time in human_times:
            if (times[frame]== time):
                human_line.set_xdata(human_x_pos[:frame])
                human_line.set_ydata(human_y_pos[:frame])
                #print(times[frame], time)
        #
        return (husky_line, human_line)


    ani = animation.FuncAnimation(fig=fig, func=update, frames=len(husky_x_pos), interval=30)

### Slider position plot **IS NOT CALLED, implemented in main method**
def sliderPositionPlot(ax, fig, husky_x_pos, husky_y_pos, human_x_pos, human_y_pos, minX, minY, maxX, maxY, minT, maxT, times, human_times):

    slider_husky_line = ax[0,1].plot(husky_x_pos[0], husky_y_pos[0], label=f"Husky")[0]
    slider_human_line = ax[0,1].plot(human_x_pos[0], human_y_pos[0], label=f"Human")[0]
    #sliderplot = ax[1,1].plot(husky_x_pos, husky_y_pos)
    ax[0,1].set(xlim=[minX-1, 1.1*maxX], ylim=[minY-1,1.1*maxY], xlabel='x-position', ylabel='y-position', title = 'Slider Position Plot')
    ax[0,1].legend()


    slider_ax  = fig.add_axes([0.65, 0.70, 0.25, 0.01])
    slider = Slider(slider_ax, 'time', 0.0, maxT, valinit=0)

    def slide(val):
        idx = int(val)
        frame = times.tolist().index(idx)
        if frame < len(times):
            slider_husky_line.set_xdata(husky_x_pos[:frame])
            slider_husky_line.set_ydata(husky_y_pos[:frame])
            if times[frame] in human_times:
                slider_human_line.set_xdata(human_x_pos[:frame])
                slider_human_line.set_ydata(human_y_pos[:frame])
        fig.canvas.draw_idle()

    slider.on_changed(slide)


### velocity plots
def linVelocityPlots(ax, husky_vel_times, husky_lin_vel, human_vel_times, human_lin_vel, minLV, maxLV, minT, maxT):

    husky_vel_line = ax[1,0].plot(husky_vel_times, husky_lin_vel, label=f"Husky")[0]
    #human_vel_line = ax[1,0].plot(human_vel_times, human_lin_vel, label=f"Human")[0]
    ax[1,0].set(xlim=[minT-1, 1.1*maxT], ylim=[minLV-1, maxLV+1], xlabel='time (s)', ylabel='velocity m/s', title = 'Linear Velocity Plot')
    ax[1,0].legend()
    
    return ax

def angVelocityPlots(ax, human_vel_times, husky_ang_times, husky_ang_vel, human_ang_vel, minT, maxT, minAV, maxAV):
    husky_ang_line = ax[1,1].plot(husky_ang_times, husky_ang_vel, label=f"Husky")[0]
    #human_ang_line = ax[1,1].plot(human_vel_times, human_ang_vel, label=f"Human")[0]
    ax[1,1].set(xlim=[minT-1, 1.1*maxT], ylim=[minAV-1,maxAV+1], xlabel='time (s)', ylabel='angular velocity m/s', title = "Angular Velocity Plot")
    ax[1,1].legend()

    return ax


#print(husky_lin_vel)
def accelerationPlots(ax, husky_vel_times, husky_lin_acc, husky_ang_times, husky_ang_acc):
### Acceleration Plot
    husky_lin_acc_line = ax[2,0].plot(husky_vel_times, husky_lin_acc, label=f"Husky Linear")[0]
    husky_ang_acc_line = ax[2,0].plot(husky_ang_times, husky_ang_acc, label=f"Husky Angular", color = "lightblue")[0]

    #human_vel = ax[1,0].plot(human_vel_times, human_lin_vel, label=f"human lin vel")[0]
    ax[2,0].set(xlabel='time (s)', ylabel='acceleration m/s^2', title = 'Acceleration Plot')
    ax[2,0].legend()

    return ax



