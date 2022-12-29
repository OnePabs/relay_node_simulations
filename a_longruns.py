from simulators.A import A
from common.Distributions import Poisson
from common.Distributions import Exponential
import statistics
import os

#USER: long run parameters
min_to_millis = 60000
runtimes = [15*min_to_millis, 30*min_to_millis, 45*min_to_millis, 60*min_to_millis]
n_scalar = 3
num_repetitions = 10
mean_inter_arrival_time = 50
mean_service_time = 40
results_folder = r'C:\Users\juanp\OneDrive\Documents\projects\relay_node_simulations\simulation_results\longruns\a'
means_filepath = results_folder + os.sep + "results.txt"


#variables
simulator = A()
arrivals_distribution = Poisson(mean_inter_arrival_time)
service_time_distribution = Exponential(mean_service_time)

#write headers
f = open(means_filepath, 'w')
f.write("runtime,")
f.write("repetitions,")
f.write("buffer mean arrival rate,")
f.write("buffer arrival rate stdev,")
f.write("storage manager mean service time,")
f.write("storage manager service time stdev,")
f.write("buffer mean residence time,")
f.write("buffer residence time stdev,")
f.write("storage manager mean residence time,")
f.write("storage manager residence time stdev,")
f.write("E mean,")
f.write("E stdev,")
f.write("\n")
f.close()

# perform long runs
for runtime in runtimes:
    n = int(runtime/mean_inter_arrival_time)*n_scalar
    print(n)
    list_of_mean_arrival_rates = []
    list_of_mean_service_times = []
    list_of_buffer_res_times = []
    list_of_sm_res = []
    list_of_mean_Es = []
    for rep in range(num_repetitions):
        exp_result = A.run(n, arrivals_distribution, service_time_distribution)
        list_of_mean_arrival_rates.append(1000/exp_result["ia_buff"])
        list_of_mean_service_times.append(exp_result["st_storage"])
        list_of_buffer_res_times.append(0)
        list_of_sm_res.append(exp_result["res_sm"])
        list_of_mean_Es.append(exp_result["E"])
    # write all the data collected
    datapath = results_folder + os.sep + "raw_data_rt_" + str(runtime) + ".txt"
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

    st_mean = statistics.mean(list_of_mean_service_times)
    st_stdev = statistics.stdev(list_of_mean_service_times, xbar=st_mean)

    buffer_res_mean = statistics.mean(list_of_buffer_res_times)
    buffer_res_stdev = statistics.stdev(list_of_buffer_res_times, xbar=buffer_res_mean)

    sm_res_mean = statistics.mean(list_of_sm_res)
    sm_res_stdev = statistics.stdev(list_of_sm_res, xbar=sm_res_mean)

    E_mean = statistics.mean(list_of_mean_Es)
    E_stdev = statistics.stdev(list_of_mean_Es, xbar=E_mean)

    # write results to file
    f = open(means_filepath, "a")
    f.write(str(runtime))
    f.write(",")
    f.write(str(num_repetitions))
    f.write(",")
    f.write(str(ar_mean))
    f.write(",")
    f.write(str(ar_stdev))
    f.write(",")
    f.write(str(st_mean))
    f.write(",")
    f.write(str(st_stdev))
    f.write(",")
    f.write(str(buffer_res_mean))
    f.write(",")
    f.write(str(buffer_res_stdev))
    f.write(",")
    f.write(str(sm_res_mean))
    f.write(",")
    f.write(str(sm_res_stdev))
    f.write(",")
    f.write(str(E_mean))
    f.write(",")
    f.write(str(E_stdev))
    f.write("\n")
    f.close()




