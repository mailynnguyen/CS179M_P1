import math
import copy
from numpy import random
import numpy as np
import msvcrt
import matplotlib.pyplot as plt
    

def euclidean_distance(c1, c2):
    return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)


def create_distance_matrix(input_file, num_nodes):
    data_file = open(input_file, "r") # open the input file into a variable called data_file
    coordinates = [] # coordinates variable to store all the coordinates
    for line in data_file:
        coordinates.append([float(c) for c in line.strip().split()]) # ['number', 'number']

    distance_matrix = [[0] * num_nodes for _ in range(num_nodes)]
    for x in range(num_nodes):
        for y in range(num_nodes):
            distance_matrix[x][y] = euclidean_distance(coordinates[x], coordinates[y])
    return distance_matrix, coordinates
    # print(distance_matrix)


def calc_nearest_neighbor(distance_matrix, num_nodes):
    total_distance = 0
    visited = [0] # array to hold all the visited nodes
    i = 0 # i = current node/point
    while len(visited) != num_nodes: # looping through all indexes/rows/points
        nearest_neighbor_distance = float('inf') # current nearest neighbor distance is inf
        for j in range(num_nodes): # looping thorugh all points/columns

            if i != j and j not in visited: # if the point is not the same as the curr point and has not been visited yet
                neighbor_distance = distance_matrix[i][j] # check the distance from the curr point to the neighboring point

                if neighbor_distance < nearest_neighbor_distance: # if the distance from curr point to neighboring point is less than the smallest neighboring distance
                    nearest_neighbor_distance = neighbor_distance # assign that to be the nearest neighbor distance
                    nearest_neighbor = j # make the neighboring point to be the designated nearest neighbor

        total_distance += nearest_neighbor_distance # add up the total distance using the shortest nearest neighbor position
        visited.append(nearest_neighbor) # add that point to visited 
        i = nearest_neighbor # make the curr point the nearest neighbor point

    total_distance += distance_matrix[i][0] # add up the distance from the ending point to the starting point

    # print(total_distance)

    return visited, total_distance


def calc_nearest_neighbor_with_solution(distance_matrix, curr_solution, shortest_distance):
    total_distance = 0
    curr_node = curr_solution[0] # set the curr node to be the first node in the solution, which is the starting node, should be 0
    for next_node in curr_solution: # loop through all the nodes in the solution 
        total_distance += distance_matrix[curr_node][next_node] # find the distance btw the curr node and the next node and add to total distance
        if total_distance > shortest_distance: # early abandoning
                break
        curr_node = next_node # set the curr node to be the next node (the next node will move forward)
    total_distance += distance_matrix[curr_node][0] # add the distance of the last node to the first to the total distance

    return total_distance


def write_to_text_file(input_file, shortest_solution, coordinates):
    with open(f"{input_file.replace('.txt', '')}_solution.txt", "w") as output_file:
        for node in shortest_solution:
            output_file.write(" ".join(f"{_:.7e}" for _ in coordinates[node]) + "\n")

    # with open(f"{input_file.replace('.txt', '')}_solution.txt", "r") as file:
    #     print(file.read())

    return f"{input_file.replace('.txt', '')}_solution.txt"


def create_solution_visual(output_file_name):
    data_file = open(output_file_name, "r") # open the input file into a variable called data_file
    coordinates = [] # coordinates variable to store all the coordinates
    for line in data_file:
        coordinates.append([float(c) for c in line.strip().split()]) # ['number', 'number']

    x, y = zip(*coordinates)

    plt.figure()
    plt.plot(x, y, 'o-')

    plt.show()



def main():
    print("ComputeDronePath")
    input_file = input("Enter the name of file: ")
    data_file = open(input_file, "r")
    num_nodes = 0
    for _ in data_file:
        num_nodes += 1
    print(f"There are {num_nodes} nodes, computing route..")
    print("\tShortest Route Discovered So Far")

    distance_matrix, coordinates = create_distance_matrix(input_file, num_nodes) # creates a distance matrix that holds the distance between node x and y at distance_matrix[x][y]

    # RANDOM SEARCH
    # shortest_distance = float('inf')

    # for _ in range(1000000):
    #     og_arr = np.array((range(1, num_nodes + 1)))
    #     random.shuffle(og_arr[1:])
    #     new_arr = np.append(og_arr, 1)

        
    #     total_distance = 0
    #     curr_point = new_arr[0]
    #     for next_point in new_arr:
    #         total_distance += distance_matrix[curr_point - 1][next_point - 1]
    #         if total_distance > shortest_distance:
    #             break
    #         curr_point = next_point
    #     # print(total_distance)

    #     if total_distance < shortest_distance:
    #         shortest_distance = total_distance
    #         print(shortest_distance)

    # i = 0
    # for row in distance_matrix:
    #     print(f"{i}: {row}")
    #     i += 1

    # NEAREST NEIGHBOR
    shortest_solution, shortest_distance = calc_nearest_neighbor(distance_matrix, num_nodes)
    print(f"\t\t{shortest_distance}")

    while True:
        if msvcrt.kbhit(): # checks if key has been hit
            key = msvcrt.getwche() # gets the char pressed
            if key == '\r': # '\r' represents the 'Enter' key
                break

        solution = copy.deepcopy(shortest_solution) # copy the shortest solutiont to use

        # randomizes two nodes that are close together
        node1 = random.randint(1, num_nodes) # get a randon first node, doesn't choose the starting node
        if node1 < num_nodes - 3:
            node2 = node1 + 3
        else:
            node2 = node1 - random.randint(1, 3)
        
        # randomizes randonmly distanced nodes
        # node1 = random.randint(1, num_nodes)
        # node2 = random.randint(1, num_nodes)
        # while node2 == node1:
        #     node2 = random.randint(1, num_nodes)


        solution[node1], solution[node2] = solution[node2], solution[node1] # swap the two nodes

        total_distance = calc_nearest_neighbor_with_solution(distance_matrix, solution, shortest_distance) # calcs the nearest neighbor with the swapped solution and returns the total distance

        if total_distance < shortest_distance:
            shortest_distance = total_distance
            shortest_solution = solution
            print(f"\t\t{shortest_distance}")

    output_file_name = write_to_text_file(input_file, shortest_solution, coordinates)

    create_solution_visual(output_file_name)

    print(f"Route written to disk as {output_file_name}")
        


main()