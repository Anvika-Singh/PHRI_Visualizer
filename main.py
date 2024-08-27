
import rosbag
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
import numpy as np


import graphs
import getMessages
import metrics 
import transformations




#bag_name = input("what bag?")
bag_name = "PHRI_bagfiles_2024-05-30-20-08-28.bag"
bag = rosbag.Bag("/home/anvikaks/Downloads/" + bag_name)
topics = bag.get_type_and_topic_info()[1].keys()

"""
'2024-05-24-11-54-02(1).bag'
 2024-05-24-16-43-44.bag
 PHRI_bagfiles_2024-05-30-20-03-13.bag
 PHRI_bagfiles_2024-05-30-20-04-13.bag
'PHRI_bagfiles_2024-05-30-20-05-19(1).bag'
 PHRI_bagfiles_2024-05-30-20-05-19.bag
 PHRI_bagfiles_2024-05-30-20-08-28.bag
 #weird PHRI_bagfiles_2024-05-30-20-09-28.bag
 PHRI_bagfiles_2024-05-30-20-10-43.bag
 PHRI_bagfiles_2024-05-30-20-10-43.KrA_ppfl.bag.part
 PHRI_bagfiles_2024-05-30-20-11-28.bag
 PHRI_bagfiles_2024-05-30-20-11-28.YES9wRE7.bag.part

"""

# graph bounds

minX = 0
maxX = 0

minY = 0
maxY = 0

minT = 0
maxT = 0

minLV = 0
maxLV = 0

minAV = 0
maxAV = 0

# prints the message about husky positioning
times, husky_x_pos, husky_y_pos, minX, maxX, minY, maxY = getMessages.huskyPosition(bag, minX, maxX, minY, maxY)
finalPosition = [husky_x_pos[-1], husky_y_pos[-1]]


# prints the message about human positioning and speed to a file
husky_vel_times, husky_ang_vel, husky_lin_vel, minLV, maxLV, minAV, maxAV = getMessages.huskyVelocity(bag, minLV, maxLV, minAV, maxAV)



# human position processing
human_times, human_x_pos, human_y_pos, minX, maxX, minY, maxY = getMessages.humanPosition(bag, minX, maxX, minY, maxY)


#human velocity processing
human_vel_times, human_lin_vel, human_ang_vel, maxLV, minLV = getMessages.humanVelocity(bag, maxLV, minLV)

#acceleration
husky_lin_acc = []

transformations.calculateAcceleration(husky_lin_vel, husky_lin_acc)

husky_ang_acc = []

transformations.calculateAcceleration(husky_ang_vel, husky_ang_acc)




### METRICS
os.remove("temp.txt")
output = open("temp.txt", "a")
output.write("Bag: " + "TEMP\n")
output.write("\n")

## Success Metrics:
metrics.successMetrics(output)

## Quality/Social Metrics
metrics.qualityMetrics(output, husky_x_pos, husky_y_pos, human_x_pos, human_y_pos, husky_lin_acc)



# fix the times

times, husky_vel_times, human_times, human_vel_times, minT, maxT = transformations.adjustTimes(times, husky_vel_times, human_times, human_vel_times)


# fix the velocity:

husky_ang_times = husky_vel_times

transformations.removeOutliers(husky_lin_acc, husky_lin_vel, husky_vel_times, 0.1, 0.1)


#angular graph
transformations.removeOutliers(husky_ang_acc, husky_ang_vel, husky_ang_times, 0.5, 0.5)

#recalculate acceleration

husky_lin_acc = []

transformations.calculateAcceleration(husky_lin_vel, husky_lin_acc)




#Path Irregularity Index
metrics.pathIrregularityIndex(output, husky_x_pos, husky_y_pos, husky_lin_vel, husky_ang_vel, finalPosition)

### GRAPHS
### animated position plot
fig, ax = plt.subplots(3,2)

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
    return husky_line, human_line


ani = animation.FuncAnimation(fig=fig, func=update, frames=len(husky_x_pos), interval=30)

### Slider position plot
slider_husky_line = ax[0,1].plot(husky_x_pos[0], husky_y_pos[0], label=f"Husky")[0]
slider_human_line = ax[0,1].plot(human_x_pos[0], human_y_pos[0], label=f"Human")[0]
sliderplot = ax[1,1].plot(husky_x_pos, husky_y_pos)
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

ax = graphs.linVelocityPlots(ax, husky_vel_times, husky_lin_vel, human_vel_times, human_lin_vel, minLV, maxLV, minT, maxT)
ax = graphs.angVelocityPlots(ax, human_vel_times, husky_ang_times, husky_ang_vel, human_ang_vel, minT, maxT, minAV, maxAV)

### Acceleration Plot
ax = graphs.accelerationPlots(ax, husky_vel_times, husky_lin_acc, husky_ang_times, husky_ang_acc)

"""xlim=[minT-1, 1.1*maxT], ylim=[minLV, maxLV],"""
plt.tight_layout()
plt.show()
