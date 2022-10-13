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
load_factors = [1, 2/3, 0.5]
dist = MultipleBarsExponential(
                                mean_ia_for_first_part_of_cycle[0],
                                mean_ia_for_second_part_of_cycle[0],
                                n_per_cycle,
                                load_factors[0])

m = 10000               # number of files per graph
n = 50                  # number of requests per file
num_input_nodes = 5     # number of input nodes for the predictive nodes.
num_points_averaged_per_input_node = int(n/num_input_nodes)  # number of req averaged for each node = n/num_input_nodes
inputs_path = r"C:\Users\juanp\OneDrive\Documents\experiments\predictive-training\exp-inputs.csv"  # path where the inputs will be written to
labels_path = r"C:\Users\juanp\OneDrive\Documents\experiments\predictive-training\exp-labels.csv"  # path where the labels will be written to

# write headers
f_inputs = open(inputs_path, "w")
for i in range(num_input_nodes):
    f_inputs.write("input_"+str(i))
    if i < num_input_nodes - 1:
        f_inputs.write(",")
f_inputs.write("\n")
f_inputs.close()

f_labels = open(labels_path, "w")
f_labels.write("labels\n")
f_labels.close()

for load_factor_idx in range(len(load_factors)):
    for k in range(num_settings):
        dist.change_settings(mean_ia_for_first_part_of_cycle[k],
                             mean_ia_for_second_part_of_cycle[k],
                             n_per_cycle,
                             load_factors[load_factor_idx])
        for i in range(m):
            data = dist.create(n, write_to_file=False)
            # get and write inputs (averages)
            f_inputs = open(inputs_path, "a")
            for num_input_nodes_idx in range(num_input_nodes):
                avg = Sim_math_ops.average(
                    data[
                    num_input_nodes_idx * num_points_averaged_per_input_node:
                    (num_input_nodes_idx + 1) * num_points_averaged_per_input_node
                    ])
                f_inputs.write(str(avg))
                if num_input_nodes_idx < num_input_nodes-1:
                    f_inputs.write(",")
            f_inputs.write("\n")
            f_inputs.close()
            # get and write labels (predictions)
            f_labels = open(labels_path, "a")
            if load_factor_idx == 0:
                if k == 0:
                    f_labels.write("1")
                else:
                    f_labels.write("0")
            elif load_factor_idx == 1:
                if k == 0:
                    f_labels.write("0")
                else:
                    f_labels.write("1")
            elif load_factor_idx == 2:
                if k == 0:
                    f_labels.write("0")
                else:
                    f_labels.write("1")
            f_labels.write("\n")
            f_labels.close()



# note:

# 0-0-x: predict C
# 0-1-x: predict A
# 1-0-x: predict A
# 1-1-x: predict C
# 2-0-x: predict A
# 2-1-x: predict C

