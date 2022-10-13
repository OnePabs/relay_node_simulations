from simulators.Predictive import *
import time


is_verbose = False

# model parameters
# saved_model_path = r"C:\Users\juanp\OneDrive\Documents\experiments\predictive_models\constant"
saved_model_path = r"C:\Users\juanp\OneDrive\Documents\experiments\predictive_models\exponential"

# Experiment Parameters
m = 10           # number of experiments
n = 100000     # number of requests per experiment
t = 3           # threshold number of requests before data transfer happens


# arrivals parameters
# high_values = [330, 200, 143, 100, 77, 50]  # high ia values (low rate) experiment
high_values = [100]   # default high value

low_values = [67] #[77, 50, 47, 45, 44]   # low ia values (high rate) experiment
# low_values = [50]   # default load factor

# load_factors = [0, 0.25, 0.5, 0.75, 1]  # load factor experiment
load_factors = [0.5]  # default load factor


# service time parameters
mean_service_time = 40
service_time_distribution = Exponential(mean_service_time)

# results parameters
results_path = r"C:\Users\juanp\OneDrive\Documents\experiments\temp\mult-bars-poisson\high_rate_experiments\predictive\m10-n100thous-t3-1.txt"


# Load Factor Experiment
I_values = [100000]

# I values experiment
# [50, 500, 5000, 50000, 500000]
# I_values = [50, 500, 1000]
# I_values.extend(list(range(2500, 20000, 2500)))
# I_values.extend(list(range(20000, 50001, 10000)))
# I_values.extend([100000, 200000, 500000])

f = open(results_path, "w")
f.write("Load Factor, I_value, high_ia, low_ia, Average E (milliseconds), e1, e2, e3, e4, e5, e6, e7, e8, e9, e10")
f.write("\n")
f.close()

total_num_exp = len(high_values)*len(low_values)*len(load_factors)*len(I_values)
idx = 0
for I_value in I_values:
    idx += 1
    print("working on experiment: " + str(idx) + " out of " + str(total_num_exp))
    print("working on I value: " + str(I_value))

    for load_factor in load_factors:
        print("working on load factor: " + str(load_factor))
        for high_value in high_values:
            for low_value in low_values:
                start_time = time.time()
                arrival_times_distribution = MultipleBarsPoisson(high_value, low_value, I_value, load_factor)
                Es = []
                for i in range(m):
                    E = Predictive.run(n=n,
                                       t=t,
                                       model_filepath=saved_model_path,
                                       arrivals_distribution=arrival_times_distribution,
                                       service_time_distribution=service_time_distribution)
                    Es.append(E)
                avg_E = Sim_math_ops.average(Es)

                end_time = time.time()
                duration = end_time - start_time
                print("Experiment duration: " + str(duration))
                print()

                # write results
                f = open(results_path, "a")
                f.write(str(load_factor) + ",")
                f.write(str(I_value) + ",")
                f.write(str(high_value) + ",")
                f.write(str(low_value) + ",")
                f.write(str(avg_E) + ",")
                for k in range(len(Es)):
                    f.write(str(Es[k]) + ",")
                f.write("\n")
                f.close()


