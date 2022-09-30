from common.Distributions import *
from common.Sim_math_ops import Sim_math_ops

# variables
mean_ia_for_first_part_of_cycle = [50, 100]
mean_ia_for_second_part_of_cycle = [100, 50]
if len(mean_ia_for_first_part_of_cycle) == len(mean_ia_for_second_part_of_cycle):
    num_settings = len(mean_ia_for_first_part_of_cycle)
else:
    print("different number of first part and second part experiments")
    exit()
n_per_cycle = 50
load_factor = 1
dist = MultipleBarsExponential(mean_ia_for_first_part_of_cycle[0], mean_ia_for_second_part_of_cycle[0], n_per_cycle, load_factor)

m = 1000                # number of files per graph
n = 50                  # number of requests per file
num_input_nodes = 5     # number of input nodes for the predictive nodes.
num_points_averaged_per_input_node = int(n/num_input_nodes)  # number of req averaged for each node = n/num_input_nodes
path = r"C:\Users\juanp\OneDrive\Documents\experiments\predictive-training\data.csv"

# write headers
f = open(path,"w")
for i in range(num_input_nodes):
    f.write("input_"+str(i)+",")
f.write("prediction\n")
f.close()


# all same inter arrival time
for k in range(num_settings):
    dist.change_settings(mean_ia_for_first_part_of_cycle[k],
                         mean_ia_for_second_part_of_cycle[k],
                         n_per_cycle,
                         load_factor)
    for i in range(m):
        data = dist.create(n, write_to_file=False)
        # get and write averages
        f = open(path, "a")
        for num_input_nodes_idx in range(num_input_nodes):
            avg = Sim_math_ops.average(
                data[
                    num_input_nodes_idx*num_points_averaged_per_input_node:
                    (num_input_nodes_idx+1)*num_points_averaged_per_input_node
                ])
            f.write(str(avg)+",")
        if k == 0:
            f.write("1")
        else:
            f.write("0")
        f.write("\n")
        f.close()


# two thirds
load_factor = 2/3
for k in range(num_settings):
    dist.change_settings(mean_ia_for_first_part_of_cycle[k],
                         mean_ia_for_second_part_of_cycle[k],
                         n_per_cycle,
                         load_factor)
    for i in range(m):
        data = dist.create(n, write_to_file=False)
        # get and write averages
        f = open(path, "a")
        for num_input_nodes_idx in range(num_input_nodes):
            avg = Sim_math_ops.average(
                data[
                num_input_nodes_idx * num_points_averaged_per_input_node:
                (num_input_nodes_idx + 1) * num_points_averaged_per_input_node
                ])
            f.write(str(avg) + ",")
        if k == 0:
            f.write("0")
        else:
            f.write("1")
        f.write("\n")
        f.close()


# # half
load_factor = 0.5
for k in range(num_settings):
    dist.change_settings(mean_ia_for_first_part_of_cycle[k],
                         mean_ia_for_second_part_of_cycle[k],
                         n_per_cycle,
                         load_factor)
    for i in range(m):
        data = dist.create(n, write_to_file=False)
        # get and write averages
        f = open(path, "a")
        for num_input_nodes_idx in range(num_input_nodes):
            avg = Sim_math_ops.average(
                data[
                num_input_nodes_idx * num_points_averaged_per_input_node:
                (num_input_nodes_idx + 1) * num_points_averaged_per_input_node
                ])
            f.write(str(avg) + ",")
        if k == 0:
            f.write("0")
        else:
            f.write("1")
        f.write("\n")
        f.close()


# note:

# 0-0-x: predict C
# 0-1-x: predict A
# 1-0-x: predict A
# 1-1-x: predict C
# 2-0-x: predict A
# 2-1-x: predict C

