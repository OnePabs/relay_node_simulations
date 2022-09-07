# Creates inter arrival requests with the following distribution
# First the request arrive at a low rate (high ia), then the request arrive at a high rate (low ia)

from DistributionCreator import DistributionCreator
import math

filepath = r"C:\Users\juanp\OneDrive\Documents\experiments\temp\temp.txt"
max_experiment_time = 1000
load_factor = 0.5               # the fraction of time the low rate is used
slow_inter_arrival_time = 100   # the low rate inter arrival time
fast_inter_arrival_time = 50    # the high rate inter arrival time
# distribution = "EXPONENTIAL"
#distribution = "POISSON"
#distribution = "CONSTANT"
distribution = "CONSTANT_RUNNING_TOTAL"


n_slow = math.floor((max_experiment_time*load_factor)/slow_inter_arrival_time)
#print("nslow: " + str(n_slow))
n_high = math.floor((max_experiment_time*(1-load_factor))/fast_inter_arrival_time)
#print("n_high: " + str(n_high))

if distribution == "EXPONENTIAL":
    DistributionCreator.exponential(n_slow, slow_inter_arrival_time, filepath, False)
    DistributionCreator.exponential(n_high, fast_inter_arrival_time, filepath, True)
elif distribution == "POISSON":
    DistributionCreator.poisson(n_slow, slow_inter_arrival_time, filepath, False)
    DistributionCreator.poisson(n_high, fast_inter_arrival_time, filepath, True)
elif distribution == "CONSTANT":
    DistributionCreator.constant(n_slow,slow_inter_arrival_time,filepath,False)
    DistributionCreator.constant(n_high, fast_inter_arrival_time, filepath, True)
elif distribution == "CONSTANT_RUNNING_TOTAL":
    DistributionCreator.constant_running_total(n_slow, slow_inter_arrival_time, filepath, False)
    DistributionCreator.constant_running_total(n_high, fast_inter_arrival_time, filepath, True)






