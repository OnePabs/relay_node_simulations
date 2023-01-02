# Simulates a data trasnfer from a source node to a server node using a relay node.
# The requests are sent from the source node to the relay node
# the relay node buffers requests and periodically transfers all requests in the buffer to the server as a batch
# all requests from a same batch get serviced together

import math
from common.Sim_math_ops import Sim_math_ops
from common.Distributions import *
import statistics

class PeriodicSim:
    ###
    # n = number of requests to simulate
    # p = period at which the relay node will perform the data transfers
    # avg_service_time = average service time at the server (not at the relay node)
    # avg_inter_arrival_time = average inter arrival times at the relay node
    # isVerbose = if true, then results are printed
    @staticmethod
    def run(
            n,                                          #number of requests to simulate
            p,                                          #Period at which the relay node sends transfers
            arrivals_distribution=Poisson(50),
            service_time_distribution=Exponential(40),
            is_verbose=False
            ):
        arrival_times = arrivals_distribution.create(n)

        # Create Periods of transfer (a maximum of the time the last arrival occured plus one period will be needed)
        last_arrival = arrival_times[n - 1]
        num_periods = 0
        if last_arrival % p == 0:
            num_periods = int(last_arrival / p)
        else:
            num_periods = math.floor(last_arrival / p) + 1
        period_times = num_periods*[0]
        for i in range(num_periods):
            period_times[i] = p * (i + 1)
        #print(period_times)

        # calculate exit times from relay node
        relay_node_exit_times = n * [0]
        last_period_idx = 0
        #Since arrival_times and period_times are sorted, we can use last_period_idx
        for i in range(len(arrival_times)):
            for j in range(last_period_idx, num_periods):
                if arrival_times[i] <= period_times[j]:
                    relay_node_exit_times[i] = period_times[j]
                    break
        #print(relay_node_exit_times)

        # calculate relay node residence time
        relay_node_residence_times = n * [0]
        for i in range(n):
            relay_node_residence_times[i] = relay_node_exit_times[i] - arrival_times[i]


        # create batches as [[list of request indexes that are part of this batch],period,service_time,server_leave_time,server_queue_time]
        # we initialize the server_leave_time to zero
        batches = []
        curr_req_idx = 0
        for i in range(num_periods):
            batch = []
            # get requests that are in this batch
            req_indexes = []
            for j in range(curr_req_idx, n):
                if relay_node_exit_times[j] <= period_times[i]:
                    req_indexes.append(j)
                else:
                    curr_req_idx = j
                    break
            batch.append(req_indexes)  # append the request indexes to the batch
            batch.append(period_times[i])  # append the period to the batch
            # append server service time for batch
            if len(req_indexes) > 0:
                batch.extend(service_time_distribution.create(1))           # creates service time here
            else:
                batch.append(0)
            batch.append(0)  # append server leave time as zero. this will be calculated later
            batch.append(0)  # append queue time as zero. this will be calculated later
            batches.append(batch)  # append batch to list of batches

        if is_verbose:
            print()
            print("batches")
            print(batches)

        # calculate the server exit times for each batch
        batches[0][3] = batches[0][1] + batches[0][2]  # the first batch exit time is its period + its service time
        for i in range(1, num_periods):
            if batches[i][1] > batches[i - 1][3]:  # if batch i period is more than the previous batch exit time
                batches[i][3] = batches[i][1] + batches[i][2]  # no queuing, the exit time is the batch period + its service time
                batches[i][4] = 0
            else:
                batches[i][3] = batches[i - 1][3] + batches[i][2]  # batch has to wait until previous batch finishes execution, then has its service time.
                batches[i][4] = batches[i - 1][3] - batches[i][1]  # batch queue time is previous batch finish time - current batch arrival (or period)

        # set each request's server exit times, queue times, and service time
        server_exit_times = n * [0]
        server_queue_times = n * [0]
        server_service_times = n * [0]
        for batch in batches:
            for req_idx in batch[0]:
                server_service_times[req_idx] = batch[2]
                server_exit_times[req_idx] = batch[3]
                server_queue_times[req_idx] = batch[4]
        if is_verbose:
            print()
            print("server exit times:")
            print(server_exit_times)
            print()
            print("server_queue_times")
            print(server_queue_times)

        # calculate server residence times and end to end times
        server_residence_times = n * [0]
        end_to_end_times = n * [0]
        for i in range(n):
            server_residence_times[i] = server_exit_times[i] - relay_node_exit_times[i]
            end_to_end_times[i] = server_exit_times[i] - arrival_times[i]
        if is_verbose:
            print()
            print("server_residence_times")
            print(server_residence_times)
            print()
            print("end_to_end_times")
            print(end_to_end_times)

        # calulate averages
        avg_measured_inter_arrival_time = Sim_math_ops.avg_inter_arrival(arrival_times)
        avg_relay_node_residence_time = Sim_math_ops.average(relay_node_residence_times)
        avg_server_queue_time = Sim_math_ops.average(server_queue_times)
        avg_server_service_time = Sim_math_ops.average(server_service_times)
        avg_server_residence_time = Sim_math_ops.average(server_residence_times)
        avg_end_to_end_time = Sim_math_ops.average(end_to_end_times)

        # create dictionary
        results = {
            'ia_buff': avg_measured_inter_arrival_time,
            'st_storage': avg_server_service_time,
            'res_buff': avg_relay_node_residence_time,
            'res_sm': avg_server_residence_time,
            'E': avg_end_to_end_time
        }

        return results


# Script

# ### INPUTS ###
# m = 1                                             #number of times experiment is repeated
# n = 1000                                            #number of requests to simulate
# p = 5                                             #Period at which the relay node sends transfers
# service_dist = Constant(40)
#
# PeriodicSim.run(n,p, service_time_distribution=service_dist, is_verbose=True)

#
# ### VARIABLES TO STORE OUTPUTS ###
# avg_measured_inter_arrival_time = []
# avg_relay_node_residence_time = []
# avg_server_queue_time = []
# avg_server_service_time = []
# avg_server_residence_time = []
# avg_end_to_end_time = []
# print_all_results = True
#
# ### PERFORM EXPERIMENTS ###
# for i in range(m):
#     metrics = PeriodicSim.run(n, p, avg_inter_arrival_time, inter_arrival_times_distribution, avg_service_time, service_times_distribution, isVerbose, use_linear_service_time, mean_access_time)
#     avg_measured_inter_arrival_time.append(metrics[0])
#     avg_relay_node_residence_time.append(metrics[1])
#     avg_server_queue_time.append(metrics[2])
#     avg_server_service_time.append(metrics[3])
#     avg_server_residence_time.append(metrics[4])
#     avg_end_to_end_time.append(metrics[5])
#
# # calculate mean and stdev
#
# ### PRINT RESULTS ###
# if print_all_results:
#     print()
#     print("inputs")
#     print("input avg inter arrival time: " + str(avg_inter_arrival_time))
#     print("input avg service time: " + str(avg_service_time))
#     print()
#     print("metrics")
#     print("avg_measured_inter_arrival_time: " + str(Sim_math_ops.average(avg_measured_inter_arrival_time)))
#     print("avg_relay_node_residence_time: " + str(Sim_math_ops.average(avg_relay_node_residence_time)))
#     print("avg_server_queue_time: " + str(Sim_math_ops.average(avg_server_queue_time)))
#     print("avg_server_service_time: " + str(Sim_math_ops.average(avg_server_service_time)))
#     print("avg_server_residence_time: " + str(Sim_math_ops.average(avg_server_residence_time)))
# print("avg_end_to_end_time: " + str(Sim_math_ops.average(avg_end_to_end_time)))