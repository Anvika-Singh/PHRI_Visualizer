
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
import numpy as np


# adds to the array parameter, returning a new array with the same content as before plus some additional

def distance(x1, y1, x2, y2):
    return ((x2-x1)**2+(y2-y1)**2)**0.5

def shortest(a1, a2, a3, a4):
    shortest = len(a1)
    if (len(a2) < shortest):
        shortest = len(a2)
    if (len(a3)<shortest):
        shortest = len(a3)
    if (len(a4) < shortest):
        shortest = len(a4)
    return shortest


def compute_path_irregularity(positions, x_velocities, angular_velocities, goal):
    ###print("computing")
    length = len(positions)
    pi_index = 0.0
    current_angle = 0.0  # Assuming initial direction is along the x-axis
    
    for t in range(length):
        pos_t = np.array(positions[t])
        vel_x = x_velocities[t]
        ang_vel = angular_velocities[t]
        
        # Update the direction angle
        current_angle += ang_vel
        
        # Compute the velocity vector from x velocity and current angle
        vel_t = np.array([vel_x * np.cos(current_angle), vel_x * np.sin(current_angle)])
        goal_vec = np.array(goal) - pos_t
        
        # Normalize the vectors
        vel_t_norm = np.linalg.norm(vel_t)
        goal_vec_norm = np.linalg.norm(goal_vec)
        
        
        # Compute cos_theta without clipping
        cos_theta = np.dot(vel_t, goal_vec) / (vel_t_norm * goal_vec_norm)
        # Preserve full precision by extending the decimal places
        cos_theta = round(cos_theta, 10)
        
        # Calculate the angle
        angle = np.arccos(cos_theta)
        
        # Debug: Print intermediate values
        ###print(f"t={t}, pos_t={pos_t}, vel_t={vel_t}, goal_vec={goal_vec}, cos_theta={cos_theta}, angle={angle}")
        
        pi_index += angle
    
    return pi_index




def absSum(array):
    total = 0
    for num in array:
        total += abs(num)
    return total


def successMetrics(output):
    output.write("SUCCESS METRICS: TO BE WRITTEN \n")
    output.write("Distance to goal, path length, time to reach goal, wall collisions, human collisions, timeouts, stalled time\n")
    output.write("\n")

## Quality/Social Metrics
def qualityMetrics(output, husky_x_pos, husky_y_pos, human_x_pos, human_y_pos, husky_lin_acc):
    output.write("QUALITY AND SOCIAL METRICS:\n")
    minDist(output, husky_x_pos, husky_y_pos, human_x_pos, human_y_pos)
    totalAcceleration(output,husky_lin_acc)
    jerk(output, husky_lin_acc)

#MinDist:

def minDist(output, husky_x_pos, husky_y_pos, human_x_pos, human_y_pos):
    length = shortest(husky_x_pos, husky_y_pos, human_x_pos, human_y_pos)
    min_dist = 2000000000.0; 
    for i in range(length):
        dist = distance(husky_x_pos[i], husky_y_pos[i], human_x_pos[i], human_y_pos[i])
        if dist<min_dist:
            min_dist = dist
    output.write("Minimum Distance: " + str(min_dist) + "m\n")
    output.write("Calculates the smallest distance between the robot and the human to see if it is within the 1 m collision radius\n")
    output.write("\n")


def totalAcceleration(output, husky_lin_acc):
    total_acc = absSum(husky_lin_acc)
    output.write("Total Acceleration: " + str(total_acc) + "\n")
    output.write("Measures how smoothly the robot went. Lower is better." + "\n")
    output.write("\n")

#movement jerk
def jerk(output, husky_lin_acc):
    jerk = []
    prev = 0
    for a in husky_lin_acc:
        curr = a-prev
        jerk.append(curr)

    avg_jerk = absSum(jerk)/len(jerk)
    output.write("Avg Movement Jerk: " + str(avg_jerk) + "\n")
    output.write("Second order derivative of linear velocity to determine the jerkiness in the change of acceleration.\n")
    output.write("\n")


def pathIrregularityIndex(output, husky_x_pos, husky_y_pos, husky_lin_vel, husky_ang_vel, finalPosition):
    husky_positions = []
    for i in range(len(husky_x_pos)):
        husky_positions.append((husky_x_pos[i], husky_y_pos[i]))

    pi = compute_path_irregularity(husky_positions, husky_lin_vel, husky_ang_vel, finalPosition)

    output.write("Path Irregularity Index: " + str(pi) + "\n")
    output.write("Measures how much the robot deviates from the desired path to indicate how effiecient the path was. Lower the better" + "\n")
    output.write("\n")



"""   
#Path Irregularity Index
husky_positions = []
for i in range(len(husky_x_pos)):
    husky_positions.append((husky_x_pos[i], husky_y_pos[i]))

pi = compute_path_irregularity(husky_positions, husky_lin_vel, husky_ang_vel, finalPosition)

output.write("Path Irregularity Index: " + str(pi) + "\n")
output.write("Measures how much the robot deviates from the desired path to indicate how effiecient the path was. Lower the better" + "\n")
output.write("\n")
"""
