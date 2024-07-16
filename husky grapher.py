# %%
import rosbag
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

# %%
# adds to the array parameter, returning a new array with the same content as before plus some additional

def append(array1, word):
    length = len(array1)
    new_array = np.empty(length+1)
    for i in range(length):
        new_array[i] = array1[i]
    new_array[-1] = word
    return new_array

# %%
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

# %%
def subset(array, num):
    new_array = np.empty(num)
    for i in range(num):
        new_array[i] = array[i]
    return new_array

# %%
bag = rosbag.Bag("/home/anvikaks/Downloads/2024-05-24-16-43-44.bag")
topics = bag.get_type_and_topic_info()[1].keys()

# %%
# prints the message about husky positioning and speed to a file
os.remove("HuskyOdom.txt")
HuskyOdom_file = open("HuskyOdom.txt", "a")

for topic, msg, t in bag.read_messages(topics=['/husky_velocity_controller/odom']):
    HuskyOdom_file.write(str(msg))
    
HuskyOdom_file.close()
HuskyOdom_file = open("HuskyOdom.txt", "r")


# %%
# arrays for Husky odom

times = np.array([])
husky_x_pos = np.array([])
husky_y_pos = np.array([])
husky_ang_vel = np.array([])
husky_lin_vel = np.array([])

# %%
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
            elif count == 4:
                husky_y_pos = append(husky_y_pos, word)
                count = 0
                position = False
        elif time:
            times = append(times, word)
            time = False
        elif linear:
            count += 1
            if count == 2:
                husky_lin_vel = append(husky_lin_vel, word)
                count = 0
                linear = False
        elif angular:
            count += 1
            if count == 6:
                husky_ang_vel = append(husky_ang_vel, word)
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
        

# %%
# prints the message about human positioning and speed to a file

os.remove("HumanPose.txt")
HumanPose_file = open("HumanPose.txt", "a")

for topic, msg, t in bag.read_messages(topics=['/human/pose']):
    HumanPose_file.write(str(msg))
    
HumanPose_file.close()
HumanPose_file = open("HumanPose.txt", "r")


# %%
# arrays for human position

human_x_pos = np.array([])
human_y_pos = np.array([])

# %%
# human position processer

position= False
add = False
count = 0

for line in HumanPose_file:
    for word in line.split():
        if position:
            count+=1
            if count == 2:
                human_x_pos = append(human_x_pos, word)
            elif count == 4:
                human_y_pos = append(human_y_pos, word)
                count = 0
                position = False
        elif word == "position:":
            position = True

# %%
print("1: times, 2: ang_vel, 3: lin_vel, 5: y_pos, 6: x_pos")
x_input = input("x-axis?")
x = decide(x_input, times, ang_vel, lin_vel, y_pos, x_pos)
y_input = input("y-axis?")
y = decide(y_input, times, ang_vel, lin_vel, y_pos, x_pos)

# %%
fig, pos = plt.subplots()
temp_x = np.empty(len(husky_x_pos))
temp_y = np.empty(len(husky_y_pos))
line = pos.plot(temp_x, temp_y)
plt.show()
