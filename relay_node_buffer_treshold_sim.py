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


class RelayNodeThresholdSim:
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
    def run(n, t, avg_inter_arrival_time, inter_arrival_times_distribution, avg_service_time,
            service_times_distribution, isVerbose):
        # n accepted can only be a multiple of T so that all requests exit the relay node.
        # In the Java implementation of the system, there is a maximum period P at which, even if there aren't T requests buffered, the data transfer happens anyway
        if n % t != 0:
            n = n - n % t
            # print(n)

        # create the arrival times to the relay node
        arrival_times = n * [0]
        if inter_arrival_times_distribution.upper() == "CONSTANT":
            for i in range(1, n):  # the first arrival is taken to happen at time 0
                arrival_times[i] = arrival_times[i - 1] + Sim_math_ops.const(avg_inter_arrival_time)
        elif inter_arrival_times_distribution.upper() == "EXPONENTIAL":
            for i in range(1, n):  # the first arrival is taken to happen at time 0
                arrival_times[i] = arrival_times[i - 1] + Sim_math_ops.exp(avg_inter_arrival_time)  # exponential
        # print(arrival_times)

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
                curr_batch[1] = arrival_times[
                    i]  # set batch relay node exit time to the arrival of the last request in the batch
                batches.append(curr_batch)  # append current batch to list of batches
                curr_batch = [[], 0, 0, 0, 0]  # reset current batch to empty
        # print(batches)

        # create server service times for each batch
        if service_times_distribution.upper() == "CONSTANT":
            for i in range(len(batches)):
                batches[i][3] = Sim_math_ops.const(avg_service_time)
        elif service_times_distribution.upper() == "EXPONENTIAL":
            for i in range(len(batches)):
                batches[i][3] = Sim_math_ops.exp(avg_service_time)

        # calculate server service entry and exit times
        batches[0][2] = batches[0][1]  # for the first batch, its server service entry time is its relay node exit time
        batches[0][4] = batches[0][1] + batches[0][
            3]  # for the first batch, its server exit time is its server entry time + its server service time
        for i in range(1, len(batches)):
            if batches[i][1] > batches[i - 1][4]:
                # the batch arrived after the batch before it left the server.
                # there is no queue when the batch arrives
                batches[i][2] = batches[i][1]
            else:
                # there is a queue when the batch arrives
                batches[i][2] = batches[i - 1][
                    4]  # batch starts its service time at the time the batch before it leaves the server
            batches[i][4] = batches[i][2] + batches[i][
                3]  # batch finishes its service time at the time it starts its service time + its service time
        # print(batches)

        # calculate relay node residence times, server queue times, server residence times, and end to end times
        relay_node_residence_times = n * [0]
        server_queue_times = n * [0]
        server_service_times = n * [0]
        server_residence_times = n * [0]
        end_to_end_times = n * [0]
        for i in range(len(batches)):
            for j in batches[i][0]:
                relay_node_residence_times[j] = batches[i][1] - arrival_times[
                    j]  # request relay node residence time is the batch relay node exit time - the request arrival time
                server_queue_times[j] = batches[i][2] - batches[i][
                    1]  # batch server service entry time - batch relay node exit time
                server_service_times[j] = batches[i][4] - batches[i][
                    2]  # batch server service exit time - batch server service entry time
                server_residence_times[j] = batches[i][4] - batches[i][
                    1]  # batch server service exit time - batch relay node exit time
                end_to_end_times[j] = batches[i][4] - arrival_times[j]

        # calculate metrics
        avg_inter_arrival_time = Sim_math_ops.avg_inter_arrival(arrival_times)
        avg_relay_node_residence_time = Sim_math_ops.average(relay_node_residence_times)
        avg_server_queue_time = Sim_math_ops.average(server_queue_times)
        avg_server_service_time = Sim_math_ops.average(server_service_times)
        avg_server_residence_time = Sim_math_ops.average(server_residence_times)
        avg_end_to_end_time = Sim_math_ops.average(end_to_end_times)

        return [avg_inter_arrival_time, avg_relay_node_residence_time, avg_server_queue_time, avg_server_service_time,
                avg_server_residence_time, avg_end_to_end_time]


m = 100  # repetition of experiments
n = 10000
t = 3
mean_inter_arrival_time = 45
# nter_arrival_times_distribution = "CONSTANT"
inter_arrival_times_distribution = "EXPONENTIAL"
mean_service_time = 40
# service_times_distribution = "CONSTANT"
service_times_distribution = "EXPONENTIAL"
isVerbose = True

avg_measured_inter_arrival_times = m * [0]
avg_relay_node_residence_times = m * [0]
avg_server_queue_times = m * [0]
avg_measured_server_service_times = m * [0]
avg_server_residence_times = m * [0]
avg_end_to_end_times = m * [0]

for i in range(m):
    metrics = RelayNodeThresholdSim.run(n, t, mean_inter_arrival_time, inter_arrival_times_distribution,
                                        mean_service_time, service_times_distribution, isVerbose)
    avg_measured_inter_arrival_times[i] = metrics[0]
    avg_relay_node_residence_times[i] = metrics[1]
    avg_server_queue_times[i] = metrics[2]
    avg_measured_server_service_times[i] = metrics[3]
    avg_server_residence_times[i] = metrics[4]
    avg_end_to_end_times[i] = metrics[5]

# print("metrics: ")
# print("average measured inter arrival time: " + str(Sim_math_ops.average(avg_measured_inter_arrival_times)))
# print("avg_relay_node_residence_times: " + str(Sim_math_ops.average(avg_relay_node_residence_times)))
# print("avg_server_queue_times: " + str(Sim_math_ops.average(avg_server_queue_times)))
# print("avg_measured_server_service_times: " + str(Sim_math_ops.average(avg_measured_server_service_times)))
# print("avg_server_residence_times: " + str(Sim_math_ops.average(avg_server_residence_times)))
print("avg_end_to_end_times: " + str(Sim_math_ops.average(avg_end_to_end_times)))