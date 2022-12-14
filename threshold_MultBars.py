from simulators.ThresholdSim import ThresholdSim
from simulators.A import A
from common.Distributions import *
from common.Sim_math_ops import *
import time


is_verbose = False

m = 10           # number of experiments
n = 1000000     # number of requests per experiment
t = 1           # threshold number of requests before data transfer happens

# arrivals parameters
high_value = 100
low_value = 50
load_factor = 0.5

# service time parameters
mean_service_time = 40
service_time_distribution = Exponential(mean_service_time)

# results parameters
results_path = r"C:\Users\juanp\OneDrive\Documents\experiments\temp\mult-bars-poisson\low_50-high_100\A\n-1million-m10.txt"

# base path
base_path = r"C:\Users\juanp\OneDrive\Documents\experiments\temp"
write_to_file = False

#I_values = [50, 500, 5000, 50000, 500000]
I_values = [50, 500, 1000]
I_values.extend(list(range(2500, 20000, 2500)))
I_values.extend(list(range(20000, 100000, 10000)))
I_values.extend([100000,200000,500000])
# I_values.extend(list(range(100000, 1100000, 100000)))
# I_values.extend(list(range(1000000, 11000000,1000000)))

f = open(results_path, "w")
f.write("I_values, Average E (milliseconds), e1, e2, e3, e4, e5, e6, e7, e8, e9, e10")
f.write("\n")
f.close()

idx = 0
for I_value in I_values:
    idx += 1
    print("working on I value: " + str(I_value) + ". number " + str(idx) + " out of " + str(len(I_values)))

    I_base_path = base_path + "\\" + str(I_value)
    if write_to_file:
        print("Threshold experiment script. base path = " + I_base_path)

    start_time = time.time()

    arrival_times_distribution = MultipleBarsPoisson(high_value, low_value, I_value, load_factor)
    Es = []
    for i in range(m):
         # E = ThresholdSim.run(n, t, arrival_times_distribution, service_time_distribution,
         #                     write_to_file=write_to_file,
         #                     base_filepath=I_base_path,
         #                     is_verbose=is_verbose)
        E = A.run(n, arrival_times_distribution, service_time_distribution)
        Es.append(E)
    avg_E = Sim_math_ops.average(Es)

    end_time = time.time()
    duration = end_time - start_time
    print("Experiment duration: " + str(duration))
    print()

    # write results
    f = open(results_path, "a")
    f.write(str(I_value) + ",")
    f.write(str(avg_E) + ",")
    for k in range(len(Es)):
        f.write(str(Es[k]) + ",")
    f.write(str(avg_E) + "\n")
    f.close()
