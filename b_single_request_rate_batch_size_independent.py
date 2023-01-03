from simulators.PeriodicSim import PeriodicSim
import statistics
import os
from common.Distributions import *
import math


#USER: long run parameters
min_to_millis = 60000
runtime = 45*min_to_millis
n_scalar = 1
num_repetitions = 10
mean_inter_arrival_time = 50
mean_service_time = 40
periods = [10, 25, 50, 75, 100, 150, 300, 450, 600, 750, 900, 1050, 1200, 1350, 1500]
results_folder = r'C:\Users\juanp\OneDrive\Documents\projects\relay_node_simulations\simulation_results\single_arrival_rate_batch_size_independent\b_periods'
isExist = os.path.exists(results_folder)
if not isExist:
   os.makedirs(results_folder)
means_filepath = results_folder + os.sep + "results.txt"

#variables
simulator = PeriodicSim()
arrivals_distribution = Poisson(mean_inter_arrival_time)
service_time_distribution = Exponential(mean_service_time)
t_9 = 2.262157  # quantile of standard student t distribution that will give a CL of 95% given 9 degrees of freedom

#write headers
f = open(means_filepath, 'w')
f.write("runtime (minutes),")
f.write("period (milliseconds),")
f.write("repetitions,")
f.write("buffer mean arrival rate (requests per second),")
f.write("buffer arrival rate Margin of error (95% CL),")
f.write("storage manager mean service time (milliseconds),")
f.write("storage manager service time Margin of error (95% CL),")
f.write("buffer mean residence time (milliseconds),")
f.write("buffer residence time Margin of error (95% CL),")
f.write("storage manager mean residence time (milliseconds),")
f.write("storage manager residence time Margin of error (95% CL),")
f.write("E (milliseconds),")
f.write("E stdev,")
f.write("\n")
f.close()


# perform long runs
for period in periods:
    print(flush=True)
    print("now performing experiment for period: " + str(period) + " milliseconds", flush=True)
    n = int(runtime/mean_inter_arrival_time)*n_scalar
    # print(n)
    list_of_mean_arrival_rates = []
    list_of_mean_service_times = []
    list_of_buffer_res_times = []
    list_of_sm_res = []
    list_of_mean_Es = []
    for rep in range(num_repetitions):
        print("rep: " + str(rep), flush=True)
        exp_result = simulator.run(n, period, arrivals_distribution, service_time_distribution)
        list_of_mean_arrival_rates.append(1000/exp_result["ia_buff"])
        list_of_mean_service_times.append(exp_result["st_storage"])
        list_of_buffer_res_times.append(exp_result["res_buff"])
        list_of_sm_res.append(exp_result["res_sm"])
        list_of_mean_Es.append(exp_result["E"])
    # write all the data collected
    datapath = results_folder + os.sep + "raw_data_p_" + str(period) + ".txt"
    rf = open(datapath, "w")
    rf.write("arrival rates,")
    rf.write("storage manager service times,")
    rf.write("buffer residence times,")
    rf.write("storage manager residence time,")
    rf.write("End-to-End times\n")
    for i in range(num_repetitions):
        rf.write(str(list_of_mean_arrival_rates[i]))
        rf.write(",")
        rf.write(str(list_of_mean_service_times[i]))
        rf.write(",")
        rf.write(str(list_of_buffer_res_times[i]))
        rf.write(",")
        rf.write(str(list_of_sm_res[i]))
        rf.write(",")
        rf.write(str(list_of_mean_Es[i]))
        rf.write("\n")
    rf.close()

    # calculate means and standard dev
    ar_mean = statistics.mean(list_of_mean_arrival_rates)
    ar_stdev = statistics.stdev(list_of_mean_arrival_rates, xbar=ar_mean)
    ar_ME = t_9*(ar_stdev/math.sqrt(10))

    st_mean = statistics.mean(list_of_mean_service_times)
    st_stdev = statistics.stdev(list_of_mean_service_times, xbar=st_mean)
    st_ME = t_9*(st_stdev/math.sqrt(10))

    buffer_res_mean = statistics.mean(list_of_buffer_res_times)
    buffer_res_stdev = statistics.stdev(list_of_buffer_res_times, xbar=buffer_res_mean)
    buffer_res_ME = t_9*(buffer_res_stdev/math.sqrt(10))

    sm_res_mean = statistics.mean(list_of_sm_res)
    sm_res_stdev = statistics.stdev(list_of_sm_res, xbar=sm_res_mean)
    sm_res_ME = t_9*(sm_res_stdev/math.sqrt(10))

    E_mean = statistics.mean(list_of_mean_Es)
    E_stdev = statistics.stdev(list_of_mean_Es, xbar=E_mean)
    E_ME = t_9*(E_stdev/math.sqrt(10))

    # write results to file
    f = open(means_filepath, "a")
    f.write(str(runtime/min_to_millis))
    f.write(",")
    f.write(str(period))
    f.write(",")
    f.write(str(num_repetitions))
    f.write(",")
    f.write(str(ar_mean))
    f.write(",")
    f.write(str(ar_ME))
    f.write(",")
    f.write(str(st_mean))
    f.write(",")
    f.write(str(st_ME))
    f.write(",")
    f.write(str(buffer_res_mean))
    f.write(",")
    f.write(str(buffer_res_ME))
    f.write(",")
    f.write(str(sm_res_mean))
    f.write(",")
    f.write(str(sm_res_ME))
    f.write(",")
    f.write(str(E_mean))
    f.write(",")
    f.write(str(E_ME))
    f.write("\n")
    f.close()


