from common.Distributions import *
import matplotlib.pyplot as plt
from simulators.A import A

# c = Constant(5)
# c.create(5,True,r"C:\Users\juanp\OneDrive\Documents\experiments\temp\test.txt",True)

# Multiple Bars
# high = 10000
# low = 1000
# n_per_cycle = 20000
# load_factor = 0.5
# m = MultipleBarsPoisson(high, low, n_per_cycle, load_factor)
#
# # create arrival times
# num_cycles = 2
# write_to_file = False
# arrivals = m.create(num_cycles, write_to_file)
#
# # calculate inter arrival times
# inter_arrivals = (len(arrivals)-1)*[0]
# for i in range(len(inter_arrivals)):
#     inter_arrivals[i] = arrivals[i+1] - arrivals[i]
#
# # plot inter arrival times
# x_points = range(len(arrivals))
# plt.scatter(x_points, arrivals)
# plt.show()


#Poisson
# mean = 50
# p = Poisson(mean)
# arrivals = p.create(100000)
# x_points = range(len(arrivals))
# plt.scatter(x_points, arrivals)
# plt.show()

# arrivals_distribution = Poisson(50)
# service_times_distribution = Exponential(40)
# a = A.run(10000)
# print(a)


from simulators.ThresholdSim import ThresholdSim

results = ThresholdSim.run(3, 3, service_time_distribution=Constant(40))
print("Mean buff res time: " + str(results['res_buff']))
print("Mean Storage Cloud res time: " + str(results['res_sm']))
print("Mean E time: " + str(results['E']))






