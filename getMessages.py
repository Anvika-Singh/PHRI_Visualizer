import numpy as np


def huskyPosition(bag, minX, maxX, minY, maxY):
    times = []
    husky_x_pos = []
    husky_y_pos = []
    for topic, msg, t in bag.read_messages(topics=['/husky_velocity_controller/odom']):
        times.append(msg.header.stamp.secs)
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        husky_x_pos.append(x)
        husky_y_pos.append(y)

        if (x>maxX):
            maxX = x
        elif (x<minX):
            minX = x
        if (y>maxY):
            maxY = y
        elif (y<minY):
            minY = y

    times = np.asarray(times)
    husky_x_pos = np.asarray(husky_x_pos)
    husky_y_pos = np.asarray(husky_y_pos)

    return times, husky_x_pos, husky_y_pos, minX, maxX, minY, maxY


def huskyVelocity(bag, minLV, maxLV, minAV, maxAV):
    # husky velocity
    husky_ang_vel = []
    husky_lin_vel = []
    husky_vel_times = []
    for topic, msg, t in bag.read_messages(topics=['/husky_velocity_controller/cmd_vel']):
        time_secs = int(t.to_sec())
        husky_vel_times.append(time_secs)

        
        av = msg.angular.z
        lv = msg.linear.x
        husky_ang_vel.append(av)
        husky_lin_vel.append(lv)


        if (lv>maxLV):
            maxLV = lv
        elif (lv<minLV):
            minLV = lv
        if (lv>maxLV):
            maxLV = lv
        elif (lv<minLV):
            minLV = lv

        if (av>maxAV):
            maxAV = av
        elif (av<minAV):
            minAV = av
        if (av>maxAV):
            maxAV = av
        elif (av<minAV):
            minAV = av
    husky_vel_times = np.asarray(husky_vel_times)
    husky_lin_vel = np.asarray(husky_lin_vel)
    husky_ang_vel = np.asarray(husky_ang_vel)

    return husky_vel_times, husky_ang_vel, husky_lin_vel, minLV, maxLV, minAV, maxAV


def humanPosition(bag, minX, maxX, minY, maxY):
    # arrays for human position
    human_x_pos = []
    human_y_pos = []
    human_times = []
    for topic, msg, t in bag.read_messages(topics=['/human/pose']):
        human_times.append(msg.header.stamp.secs)
        x = msg.pose.position.x
        y = msg.pose.position.y
        human_x_pos.append(x)
        human_y_pos.append(y)

        if (x>maxX):
            maxX = x
        elif (x<minX):
            minX = x
        if (y>maxY):
            maxY = y
        elif (y<minY):
            minY = y

    human_times = np.asarray(human_times)
    human_x_pos = np.asarray(human_x_pos)
    human_y_pos = np.asarray(human_y_pos)

    return human_times, human_x_pos, human_y_pos, minX, maxX, minY, maxY

def humanVelocity(bag, maxLV, minLV):
    # arrays for human vel
    human_lin_vel = []
    human_ang_vel = []
    human_vel_times = []
    for topic, msg, t in bag.read_messages(topics=['/human/twist']):
        human_vel_times.append(msg.header.stamp.secs)
        xvel = msg.twist.linear.x
        yvel = msg.twist.linear.y
        netvel = (xvel**2 + yvel**2) ** 0.5
        human_lin_vel.append(netvel)

        if (netvel>maxLV):
            maxV = netvel
        elif (netvel<minLV):
            minLV = netvel
        if (netvel>maxLV):
            maxLV = netvel
        elif (netvel<minLV):
            minLV = netvel

        avel= np.arcsin(yvel * 1 / netvel)
        human_ang_vel.append(avel)
        # ang velocity --> sin(ang)/ydirection = sin(90)/netvel

    human_vel_times = np.asarray(human_vel_times)
    human_lin_vel = np.asarray(human_lin_vel)
    human_ang_vel = np.asarray(human_ang_vel)

    return human_vel_times, human_lin_vel, human_ang_vel, maxLV, minLV
