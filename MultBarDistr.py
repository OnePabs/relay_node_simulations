# Creates inter arrival requests with the following distribution
# First the request arrive at a low rate (high ia), then the request arrive at a high rate (low ia)

from DistributionCreator import DistributionCreator
import math

filepath = r"C:\Users\juanp\OneDrive\Documents\experiments\temp\temp.txt"
max_experiment_time = 100
I = 500
slow_inter_arrival_time = 100   # the low rate inter arrival time
fast_inter_arrival_time = 50    # the high rate inter arrival time
# distribution = "EXPONENTIAL"
#distribution = "POISSON"
#distribution = "CONSTANT"
distribution = "CONSTANT_RUNNING_TOTAL"


n_slow = math.floor(I/slow_inter_arrival_time)
n_high = math.floor(I/fast_inter_arrival_time)
append = False
for idx in range(0,I,max_experiment_time):
    if distribution == "EXPONENTIAL":
        DistributionCreator.exponential(n_slow, slow_inter_arrival_time, filepath, append)
        DistributionCreator.exponential(n_high, fast_inter_arrival_time, filepath, True)
    elif distribution == "POISSON":
        DistributionCreator.poisson(n_slow, slow_inter_arrival_time, filepath, append)
        DistributionCreator.poisson(n_high, fast_inter_arrival_time, filepath, True)
    elif distribution == "CONSTANT":
        DistributionCreator.constant(n_slow,slow_inter_arrival_time,filepath,append)
        DistributionCreator.constant(n_high, fast_inter_arrival_time, filepath, True)
    elif distribution == "CONSTANT_RUNNING_TOTAL":
        print("CONSTANT_RUNNING_TOTAL " + str(append))
        DistributionCreator.constant_running_total(n_slow, slow_inter_arrival_time, filepath, append)
        DistributionCreator.constant_running_total(n_high, fast_inter_arrival_time, filepath, True)
    append = True






