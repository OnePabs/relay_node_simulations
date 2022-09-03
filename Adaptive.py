# Adaptive
# the adaptive technique is used by the relay node to switch between techniques A and C depending on the relay node request arrival rate

from Sim_math_ops import Sim_math_ops
from DistributionCreator import DistributionCreator

class Adaptive:


    # Returns:
    # [0] avg_inter_arrival_time
    # [1] avg_relay_node_residence_time
    # [2] avg_server_queue_time
    # [3] avg_server_residence_time
    @staticmethod
    def run(
            switch_ia_thrsh,                # inter arrival time at witch the adaptive technique switches from using technique A to Technique C and vice versa
            NPIAC,                           # number of requests considered in order to take the decision to change technique or keep using the same technique
            c_thrsh,                        # When technique C is used, c_thrsh is the number of requests buffered at the relay node until a data transfer happen
            arrival_times_filepath,
            service_times_filepath,
            isVerbose=False
    ):
        arrival_times = DistributionCreator.read(arrival_times_filepath)
        st_times = DistributionCreator.read(service_times_filepath)

        #check that the number of ia arrivals is the same as the number of service times created
        if len(arrival_times) != len(st_times):
            print("ERROR: number of arrivals and number of service times do not match")
            return

        #calculate the average inter arrival time of the last NPRC requests for each new arrival
        num_requests = len(arrival_times)
        ia_avgs = (num_requests-1)*[0]
        ia_sums = (num_requests-1)*[0]
        #first we calculate the average inter arrival time of the last NPIAC requests for request numbers at and below NPIAC. In this case, all previous requests are taken into account for the average
        new_inter_arrival = arrival_times[1] - arrival_times[0]
        ia_avgs[0] = new_inter_arrival
        ia_sums[0] = new_inter_arrival
        for i in range(1,NPIAC):
            new_inter_arrival = arrival_times[i+1] - arrival_times[i]
            ia_sums[i] = ia_sums[i-1] + new_inter_arrival #previous sum plus new inter arrival time
            ia_avgs[i] = ia_sums[i]/(i+1)
        #then we calculate the average inter arrival time of the last NPIAC requests for request numbers above NPIAC
        for i in range(NPIAC,num_requests):
            new_inter_arrival = arrival_times[i + 1] - arrival_times[i]
            ia_sums[i] = ia_sums[i-1] + new_inter_arrival - ia_sums[i-NPIAC]  #previous sum + new inter arrival - the sum of the requests that are more than NPIAC inter arrivals away from this newest one
            ia_avgs[i] = ia_sums[i] / NPIAC

        # calculate metrics
        # avg_inter_arrival_time = Sim_math_ops.avg_inter_arrival(arrival_times)
        # avg_relay_node_residence_time = Sim_math_ops.average(relay_node_residence_times)
        # avg_server_queue_time = Sim_math_ops.average(server_queue_times)
        # avg_server_service_time = Sim_math_ops.average(server_service_times)
        # avg_server_residence_time = Sim_math_ops.average(server_residence_times)
        # avg_end_to_end_time = Sim_math_ops.average(end_to_end_times)
        #
        # return [avg_inter_arrival_time, avg_relay_node_residence_time, avg_server_queue_time, avg_server_service_time,
        #         avg_server_residence_time, avg_end_to_end_time]
        return


# m = 100  # repetition of experiments
# n = 1000
# t = 3
# mean_inter_arrival_time = 100
# #inter_arrival_times_distribution = "CONSTANT"
# inter_arrival_times_distribution = "EXPONENTIAL"
# mean_service_time = 40
# #service_times_distribution = "CONSTANT"
# service_times_distribution = "EXPONENTIAL"
# isVerbose = False
#
# avg_measured_inter_arrival_times = m * [0]
# avg_relay_node_residence_times = m * [0]
# avg_server_queue_times = m * [0]
# avg_measured_server_service_times = m * [0]
# avg_server_residence_times = m * [0]
# avg_end_to_end_times = m * [0]
# print_all_results = True
#
# for i in range(m):
#     metrics = RelayNodeThresholdSim.run(n, t, mean_inter_arrival_time, inter_arrival_times_distribution,
#                                         mean_service_time, service_times_distribution, isVerbose)
#     avg_measured_inter_arrival_times[i] = metrics[0]
#     avg_relay_node_residence_times[i] = metrics[1]
#     avg_server_queue_times[i] = metrics[2]
#     avg_measured_server_service_times[i] = metrics[3]
#     avg_server_residence_times[i] = metrics[4]
#     avg_end_to_end_times[i] = metrics[5]
#
# if print_all_results:
#     print("metrics: ")
#     print("average measured inter arrival time: " + str(Sim_math_ops.average(avg_measured_inter_arrival_times)))
#     print("avg_relay_node_residence_times: " + str(Sim_math_ops.average(avg_relay_node_residence_times)))
#     print("avg_server_queue_times: " + str(Sim_math_ops.average(avg_server_queue_times)))
#     print("avg_measured_server_service_times: " + str(Sim_math_ops.average(avg_measured_server_service_times)))
#     print("avg_server_residence_times: " + str(Sim_math_ops.average(avg_server_residence_times)))
# print("avg_end_to_end_times: " + str(Sim_math_ops.average(avg_end_to_end_times)))