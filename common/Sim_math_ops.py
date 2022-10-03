import numpy as np  # linear algebra
import math

class Sim_math_ops:
    @staticmethod
    def const(value):
        return value

    # this function generates numbers that are exponentialy distributed with a mean "mean"
    # It was taken from this website: https://www.weibull.com/hotwire/issue201/hottopics201.htm
    @staticmethod
    def exp(mean):
        return (-mean * math.log(1 - np.random.uniform(0, 1)))

    # this function calculates the average of numbers inside a list
    @staticmethod
    def average(lst):
        return sum(lst) / len(lst)

    @staticmethod
    def avg_inter_arrival(lst):
        lst2 = (len(lst) - 1) * [0]
        for i in range(1, len(lst)):
            lst2[i - 1] = lst[i] - lst[i - 1]
        return Sim_math_ops.average(lst2)

    @staticmethod
    def get_inter_arrival_times(arrival_times):
        arrival_times_len = len(arrival_times)
        if arrival_times_len < 2:
            print("ERROR: less than 2 items. cannot compute inter arrival times")
            exit()
        inter_arrival_times =  (len(arrival_times)-1)*[0]
        for i in range(1, arrival_times_len):
            inter_arrival_times[i-1] = arrival_times[i] - arrival_times[i-1]
        return inter_arrival_times


