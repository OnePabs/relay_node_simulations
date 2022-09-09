# Creates inter arrival requests with the following distribution
# First the request arrive at a low rate (high ia), then the request arrive at a high rate (low ia)

from DistributionCreator import DistributionCreator
import math

class MultBarDistr:
    @staticmethod
    def run(filepath,max_experiment_time,I,slow_inter_arrival_time,fast_inter_arrival_time,distribution):
        # filepath = r"C:\Users\juanp\OneDrive\Documents\experiments\temp\temp.txt"
        # max_experiment_time = 50000000
        # I = 25000
        # slow_inter_arrival_time = 100   # the low rate inter arrival time
        # fast_inter_arrival_time = 50    # the high rate inter arrival time
        # # distribution = "EXPONENTIAL"
        # distribution = "POISSON"
        # #distribution = "CONSTANT"
        # #distribution = "CONSTANT_RUNNING_TOTAL"


        n_slow = math.floor(I/slow_inter_arrival_time)
        n_high = math.floor(I/fast_inter_arrival_time)
        append = False
        list_of_numbers = [0]
        for idx in range(0,max_experiment_time,I):
            if distribution == "EXPONENTIAL":
                list_of_numbers.extend(DistributionCreator.exponential(n_slow, slow_inter_arrival_time, "", True,list_of_numbers[-1]))
                list_of_numbers.extend(DistributionCreator.exponential(n_high, fast_inter_arrival_time, "", True,list_of_numbers[-1]))
            elif distribution == "POISSON":
                list_of_numbers.extend(DistributionCreator.poisson(n_slow, slow_inter_arrival_time, "", True,list_of_numbers[-1]))
                list_of_numbers.extend(DistributionCreator.poisson(n_high, fast_inter_arrival_time, "", True,list_of_numbers[-1]))
            elif distribution == "CONSTANT":
                list_of_numbers.extend(DistributionCreator.constant(n_slow,slow_inter_arrival_time,"",True,list_of_numbers[-1]))
                list_of_numbers.extend(DistributionCreator.constant(n_high, fast_inter_arrival_time, "", True,list_of_numbers[-1]))
            elif distribution == "CONSTANT_RUNNING_TOTAL":
                list_of_numbers.extend(DistributionCreator.constant_running_total(n_slow, slow_inter_arrival_time, "", True,list_of_numbers[-1]))
                list_of_numbers.extend(DistributionCreator.constant_running_total(n_high, fast_inter_arrival_time, "", True,list_of_numbers[-1]))

        if filepath:
            DistributionCreator.write_list_of_numbers(list_of_numbers,filepath,append)
            return
        else:
            return list_of_numbers






