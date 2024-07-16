import rosbag
import os
import matplotlib.pyplot as plt
import numpy as np

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
    
os.remove("bag.txt")

file = open("bag.txt", "a")
bag = rosbag.Bag("/home/anvikaks/Downloads/2024-05-24-16-43-44.bag")
topics = bag.get_type_and_topic_info()[1].keys()

times = np.array([])
x_pos = np.array([])
y_pos = np.array([])
ang_vel = np.array([])
lin_vel = np.array([])

for topic, msg, t in bag.read_messages(topics=['/husky_velocity_controller/odom']):
    file.write(str(msg))
    
file.close()
file = open("bag.txt", "r")


time = False
position= False
add = False
linear = False
angular = False
count = 0
x = True

for line in file:
    for word in line.split():
        if position:
            count+=1
            if count == 2:
                x_pos = append(x_pos, word)
            elif count == 4:
                y_pos = append(y_pos, word)
                count = 0
                position = False
        elif time:
            times = append(times, word)
            time = False
        elif linear:
            count += 1
            if count == 2:
                lin_vel = append(lin_vel, word)
                count = 0
                linear = False
        elif angular:
            count += 1
            if count == 6:
                ang_vel = append(ang_vel, word)
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
        

print("1: times, 2: ang_vel, 3: lin_vel, 5: y_pos, 6: x_pos")
x_input = input("x-axis?")
x = decide(x_input, times, ang_vel, lin_vel, y_pos, x_pos)
y_input = input("y-axis?")
y = decide(y_input, times, ang_vel, lin_vel, y_pos, x_pos)

fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()