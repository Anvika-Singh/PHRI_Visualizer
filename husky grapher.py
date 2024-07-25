import rosbag
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time


# adds to the array parameter, returning a new array with the same content as before plus some additional

def append(array1, word):
    length = len(array1)
    new_array = np.empty(length+1)
    for i in range(length):
        new_array[i] = array1[i]
    new_array[-1] = word
    return new_array

def decide(input, times, ang_vel, lin_vel, y_pos, x_pos):
    if input == "1":
        return times
    if input == "2":
        return ang_vel
    if input == "3":
        return lin_vel
    if input == "5":
        return y_pos
    if input == "6":
        return x_pos

bag = rosbag.Bag("/home/anvikaks/Downloads/PHRI_bagfiles_2024-05-30-20-10-43.bag")
topics = bag.get_type_and_topic_info()[1].keys()

"""
'2024-05-24-11-54-02(1).bag'
 2024-05-24-16-43-44.bag
 PHRI_bagfiles_2024-05-30-20-03-13.bag
 PHRI_bagfiles_2024-05-30-20-04-13.bag
'PHRI_bagfiles_2024-05-30-20-05-19(1).bag'
 PHRI_bagfiles_2024-05-30-20-05-19.bag
 PHRI_bagfiles_2024-05-30-20-08-28.bag
 PHRI_bagfiles_2024-05-30-20-09-28.bag
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


# prints the message about husky positioning and speed to a file
os.remove("HuskyOdom.txt")
HuskyOdom_file = open("HuskyOdom.txt", "a")

for topic, msg, t in bag.read_messages(topics=['/husky_velocity_controller/odom']):
    HuskyOdom_file.write(str(msg))
    
HuskyOdom_file.close()
HuskyOdom_file = open("HuskyOdom.txt", "r")

# arrays for Husky odom

times = np.array([])
husky_x_pos = np.array([])
husky_y_pos = np.array([])
husky_ang_vel = np.array([])
husky_lin_vel = np.array([])

# organizes the file for Husky positioning and speed by populating into arrays

time = False
position= False
add = False
linear = False
angular = False
count = 0

for line in HuskyOdom_file:
    for word in line.split():
        if position:
            count+=1
            if count == 2:
                husky_x_pos = append(husky_x_pos, word)
                if (float(word)>maxX):
                    maxX = float(word)
                elif (float(word)<minX):
                    minX = float(word)
            elif count == 4:
                husky_y_pos = append(husky_y_pos, word)
                if (float(word)>maxY):
                    maxY = float(word)
                elif (float(word)<minY):
                    minY = float(word)
                count = 0
                position = False
        elif time:
            times = append(times, word)
            if (float(word)>maxT):
                maxT = float(word)
            elif (float(word)<minT):
                minT = float(word)
            time = False
        elif linear:
            count += 1
            if count == 2:
                husky_lin_vel = append(husky_lin_vel, word)
                if (float(word)>maxLV):
                    maxLV = float(word)
                elif (float(word)<minLV):
                    minLV = float(word)
                count = 0
                linear = False
        elif angular:
            count += 1
            if count == 6:
                husky_ang_vel = append(husky_ang_vel, word)
                if (float(word)>maxAV):
                    maxAV = float(word)
                elif (float(word)<minAV):
                    minAV = float(word)
                count = 0
                angular = False

        elif word == "secs:":
            time = True
        elif word == "position:":
            position = True
        elif word == "linear:":
            linear = True
        elif word == "angular:":
            angular = True
        

# prints the message about human positioning and speed to a file

os.remove("HumanPose.txt")
HumanPose_file = open("HumanPose.txt", "a")

for topic, msg, t in bag.read_messages(topics=['/human/pose']):
    HumanPose_file.write(str(msg))
    
HumanPose_file.close()
HumanPose_file = open("HumanPose.txt", "r")


# arrays for human position

human_x_pos = np.array([])
human_y_pos = np.array([])
human_times = np.array([])

# human position processer

position= False
add = False
count = 0
time = False

for line in HumanPose_file:
    for word in line.split():
        if position:
            count+=1
            if count == 2:
                human_x_pos = append(human_x_pos, word)
                if (float(word)>maxX):
                    maxX = float(word)
                elif (float(word)<minX):
                    minX = float(word)
            elif count == 4:
                human_y_pos = append(human_y_pos, word)
                if (float(word)>maxY):
                    maxY = float(word)
                elif (float(word)<minY):
                    minY = float(word)
                count = 0
                position = False
        elif time:
            human_times = append(human_times, word)
            if (float(word)>maxT):
                maxT = float(word)
            if (float(word)<minT):
                minT = float(word)
            time = False
        elif word == "position:":
            position = True
        elif word == "secs:":
            time = True


os.remove("HumanVel.txt")
HumanVel_file = open("HumanVel.txt", "a")

for topic, msg, t in bag.read_messages(topics=['/human/twist']):
    HumanVel_file.write(str(msg))
    HumanVel_file.write("\n")
    
HumanVel_file.close()
HumanVel_file = open("HumanVel.txt", "r")


# arrays for human position

human_lin_vel = np.array([])
human_ang_vel = np.array([])
human_vel_times = np.array([])

# human velocity processer

linear= False
angular = False
count = 0
time = False

for line in HumanVel_file:
    for word in line.split():
        if time:
            human_vel_times = append(human_vel_times, word)
            if (float(word)>maxT):
                maxT = float(word)
            elif (float(word)<minT):
                minT = float(word)
            time = False
        elif linear:
            count += 1
            if count == 2:
                human_lin_vel = append(human_lin_vel, word)
                if (float(word)>maxLV):
                    maxLV = float(word)
                elif (float(word)<minLV):
                    minLV = float(word)
                count = 0
                linear = False
        elif angular:
            count += 1
            if count == 6:
                human_ang_vel = append(human_ang_vel, word)
                if (float(word)>maxAV):
                    maxAV = float(word)
                elif (float(word)<minAV):
                    minAV = float(word)
                count = 0
                angular = False

        elif word == "secs:":
            time = True
        elif word == "linear:":
            linear = True
        elif word == "angular:":
            angular = True



#fix the times

minT = times[0]

for i in range(len(times)):
    times[i] = times[i] - minT

for i in range(len(human_times)):
    human_times[i] = human_times[i] - minT

for i in range(len(human_vel_times)):
    human_vel_times[i] = human_vel_times[i] - minT

minT = 0
maxT = times[-1]









### animated position plot
fig, ax = plt.subplots(2,2)

husky_line = ax[0,0].plot(husky_x_pos[0], husky_y_pos[0], label=f"husky")[0]
human_line = ax[0,0].plot(human_x_pos[0], human_y_pos[0], label=f"human")[0]
ax[0,0].set(xlim=[minX-1, 1.1*maxX], ylim=[minY-1,1.1*maxY], xlabel='x-position', ylabel='y-position')
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


### linear velocity plot

husky_vel = ax[1,0].plot(times, husky_lin_vel, label=f"husky lin vel")[0]
human_vel = ax[1,0].plot(human_vel_times, human_lin_vel, label=f"human lin vel")[0]
ax[1,0].set(xlim=[minT-1, 1.1*maxT], ylim=[minLV, maxLV], xlabel='time (s)', ylabel='velocity m/s')
ax[1,0].legend()

husky_ang_vel = ax[0,1].plot(times, husky_ang_vel, label=f"husky ang vel")[0]
human_ang_vel = ax[0,1].plot(human_vel_times, human_ang_vel, label=f"human ang vel")[0]
ax[0,1].set(xlim=[minT-1, 1.1*maxT], ylim=[minAV,maxAV], xlabel='time (s)', ylabel='angular velocity m/s')
ax[0,1].legend()

plt.show()
