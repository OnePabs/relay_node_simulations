from common.Sim_math_ops import Sim_math_ops
from common.Distributions import *
import time

class ThresholdSim:
    ###
    # n = number of requests to simulate
    # t = after t requests have been buffered, a data transfer takes place
    # avg_service_time = average service time at the server (not at the relay node)
    # avg_inter_arrival_time = average inter arrival times at the relay node
    # isVerbose = if true, then results are printed

    # Returns:
    # [0] avg_inter_arrival_time
    # [1] avg_relay_node_residence_time
    # [2] avg_server_queue_time
    # [3] avg_server_residence_time
    @staticmethod
    def run(
            n,
            t,
            arrivals_distribution=Poisson(50),
            service_time_distribution=Exponential(40),
            isVerbose=False,
    ):
        # create arrival times
        if n % t != 0:
            n = n - n % t
            # print(n)
        arrival_times = arrivals_distribution.create(n)

        # create the appropriate batches with their request indexes.
        # calculate the relay node exit time for each batch
        # a batch has this structure:   [[request indexes],relay node exit time, server service entry time, server service time, server service exit time]
        # batch[0] = [request indexes]
        # batch[1] = relay node exit time
        # batch[2] = server service entry time
        # batch[3] = server service time
        # batch[4] = server service exit time
        batches = []
        curr_batch = [[], 0, 0, 0, 0]
        for i in range(n):
            (curr_batch[0]).append(i)  # buffer this request (increase the number of requests buffered by one)
            if len(curr_batch[0]) == t:
                # data transfer is performed
                # set batch relay node exit time to the arrival of the last request in the batch
                curr_batch[1] = arrival_times[i]
                batches.append(curr_batch)  # append current batch to list of batches
                curr_batch = [[], 0, 0, 0, 0]  # reset current batch to empty
        # print(batches)

        # create server service times for each batch
        batch_service_times = service_time_distribution.create(len(batches))
        for i in range(len(batches)):
            batches[i][3] = batch_service_times[i]

        # calculate server service entry and exit times
        batches[0][2] = batches[0][1]  # for the first batch, its server service entry time is its relay node exit time
        batches[0][4] = batches[0][1] + batches[0][3]  # for the first batch, its server exit time is its server entry time + its server service time
        for i in range(1, len(batches)):
            if batches[i][1] > batches[i - 1][4]:
                # the batch arrived after the batch before it left the server.
                # there is no queue when the batch arrives
                batches[i][2] = batches[i][1]
            else:
                # there is a queue when the batch arrives
                batches[i][2] = batches[i - 1][4]  # batch starts its service time at the time the batch before it leaves the server
            batches[i][4] = batches[i][2] + batches[i][3]  # batch finishes its service time at the time it starts its service time + its service time
        if isVerbose:
            print(batches)


        start_calc_res_times = time.time()
        # calculate relay node residence times, server queue times, server residence times, and end to end times
        #relay_node_residence_times = n * [0]
        #server_queue_times = n * [0]
        #server_service_times = n * [0]
        #server_residence_times = n * [0]
        end_to_end_times = n * [0]
        for i in range(len(batches)):
            for j in batches[i][0]:
                # request relay node residence time is the batch relay node exit time - the request arrival time
                #relay_node_residence_times[j] = batches[i][1] - arrival_times[j]
                # batch server service entry time - batch relay node exit time
                #server_queue_times[j] = batches[i][2] - batches[i][1]
                # batch server service exit time - batch server service entry time
                #server_service_times[j] = batches[i][4] - batches[i][2]
                # batch server service exit time - batch relay node exit time
                #server_residence_times[j] = batches[i][4] - batches[i][1]
                end_to_end_times[j] = batches[i][4] - arrival_times[j]


        # calculate metrics
        # avg_inter_arrival_time = Sim_math_ops.avg_inter_arrival(arrival_times)
        # avg_relay_node_residence_time = Sim_math_ops.average(relay_node_residence_times)
        # avg_server_queue_time = Sim_math_ops.average(server_queue_times)
        # avg_server_service_time = Sim_math_ops.average(server_service_times)
        # avg_server_residence_time = Sim_math_ops.average(server_residence_times)
        avg_end_to_end_time = Sim_math_ops.average(end_to_end_times)

        # return [avg_inter_arrival_time, avg_relay_node_residence_time, avg_server_queue_time, avg_server_service_time,
        #         avg_server_residence_time, avg_end_to_end_time]
        return avg_end_to_end_time



