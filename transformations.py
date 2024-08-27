import numpy as np


def calculateAcceleration(velocities, accelerations):
    vel_prev = velocities[0]
    vel_curr = 0
    for v in velocities:
        vel_curr = v
        accelerations.append(vel_curr-vel_prev)
        vel_prev = vel_curr


def adjustTimes(times, husky_vel_times, human_times, human_vel_times):
    minT = times[0]

    for i in range(len(times)):
        times[i] = times[i] - minT

    maxT = times[-1]

    for i in range(len(husky_vel_times)):
        husky_vel_times[i] = husky_vel_times[i] - minT
        if husky_vel_times[i] > maxT:
            maxT = husky_vel_times[i]

    for i in range(len(human_times)):
        human_times[i] = human_times[i] - minT
        if human_times[i] > maxT:
            maxT = human_times[i]

    for i in range(len(human_vel_times)):
        human_vel_times[i] = human_vel_times[i] - minT
        if human_vel_times[i] > maxT:
            maxT = human_vel_times[i]


    minT = 0

    return times, husky_vel_times, human_times, human_vel_times, minT, maxT


def removeOutliers(acc, vel, times, lower_bound, upper_bound):
    length = len(acc) -1
    prev = acc[0]
    i = 1
    while i < length:
        if (acc[i] > prev+upper_bound or (acc[i] < prev-lower_bound)):
            vel = np.delete(vel, i)
            times = np.delete(times, i)
            acc = np.delete(acc, i)
            length = len(acc)
        else:
            i+=1
            prev = acc[i-1]