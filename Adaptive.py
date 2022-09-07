# Adaptive
# the adaptive technique is used by the relay node to switch between techniques A and C depending on the relay node request arrival rate

from Sim_math_ops import Sim_math_ops
from DistributionCreator import DistributionCreator
from ServiceTimeSettings import *

class Adaptive:


    # Returns:
    # [0] avg_inter_arrival_time
    # [1] avg_relay_node_residence_time
    # [2] avg_server_queue_time
    # [3] avg_server_residence_time
    @staticmethod
    def run(
            switch_ia_thrsh,                # inter arrival time at witch the adaptive technique switches from using technique A to Technique C and vice versa
            NPIAC,                          # number of requests considered in order to take the decision to change technique or keep using the same technique
            c_thrsh,                        # When technique C is used, c_thrsh is the number of requests buffered at the relay node until a data transfer happen
            arrival_times_filepath,
            service_time_settings,          # one of the classes in ServiceTimeSettings file
            isVerbose=False
    ):

        arrival_times = DistributionCreator.read(arrival_times_filepath)
        #print(arrival_times)

        #calculate the average inter arrival time of the last NPRC requests for each new arrival
        ia_avgs = (len(arrival_times))*[0]
        for i in range(1,len(arrival_times)):
            if i > NPIAC:
                elapsed_time = arrival_times[i] - arrival_times[i-NPIAC]
                ia_avgs[i] = elapsed_time/NPIAC
            else:
                elapsed_time = arrival_times[i] - arrival_times[0]
                ia_avgs[i] = elapsed_time/i

        #print(ia_avgs)

        # calculate the time of leaving the relay node based on the arrival time and the technique used
        # the last time of each batch is when the batch leaves the relay node
        relay_node_exit_batches = []
        # the first request that arrives at the relay node is sent right away to the server since there are no inter arrival times to make a decision on which technique to use
        relay_node_exit_batches.append([arrival_times[0]])
        curr_technique_used = "a"
        curr_batch = []
        for i in range(1,len(arrival_times)):
            if ia_avgs[i] < switch_ia_thrsh:
                # use technique C
                if len(curr_batch) < c_thrsh:
                    curr_batch.append(arrival_times[i])
                else:
                    # batch is full. send batch and start a new one
                    relay_node_exit_batches.append(curr_batch)
                    curr_batch = [arrival_times[i]]
                curr_technique_used = "c"
            else:
                # use technique a
                if curr_technique_used == "c":
                    # send the batch that is currently being built to the server. Since technique A is being used,
                    # add the current request to the batch (the request is transmitted right away together with all the other requests buffered)
                    curr_batch.append(arrival_times[i])
                    relay_node_exit_batches.append(curr_batch)
                    curr_batch = []
                else:
                    relay_node_exit_batches.append([arrival_times[i]])
            if i == len(arrival_times)-1 and len(curr_batch)>0:
                # some requests are still batched at the end of the experiment
                relay_node_exit_batches.append(curr_batch)

        print(relay_node_exit_batches)

        #calculate relay node exit times for each request
        relay_exit_times = (len(arrival_times))*[0]
        curr_req_idx = 0
        for exit_batch in relay_node_exit_batches:
            for i in range(len(exit_batch)):
                relay_exit_times[curr_req_idx] = exit_batch[-1]
                curr_req_idx += 1
        #print(relay_exit_times)


        # calculate the relay node residence time for each request
        curr_idx = 0
        relay_node_res_times = len(arrival_times)*[0]
        for batch in relay_node_exit_batches:
            last_time_in_batch = batch[-1]
            for req_time in batch:
                relay_node_res_times[curr_idx] = last_time_in_batch - arrival_times[curr_idx]
                curr_idx += 1

        #print(relay_node_res_times)

        # create the service times for each batch
        service_times = []
        if isinstance(service_time_settings,ConstantDistributionSettings):
            DistributionCreator.constant(len(relay_node_exit_batches),service_time_settings.const,service_time_settings.filepath,False)
            service_times = DistributionCreator.read(service_time_settings.filepath)
        else:
            raise Exception('Service Time Distribution', 'Not Found')

        #print(service_times)

        # calculate the time of leaving the server for each request
        batch_server_exit_times = (len(service_times))*[0]
        batch_server_service_start_time = (len(service_times))*[0]
        batch_server_exit_times[0] = relay_node_exit_batches[0][-1] + service_times[0]
        for i in range(1,len(service_times)):
            if relay_node_exit_batches[i][-1] < batch_server_exit_times[i-1]:       #batch arrived before previous batched finished processing
                batch_server_exit_times[i] = batch_server_exit_times[i-1] + service_times[i] #batch starts processing when previous batch finishes, and takes service_times[i] to finish
                batch_server_service_start_time[i] = batch_server_exit_times[i-1]
            else:
                # batched arrived and there was no queue. process right away
                batch_server_exit_times[i] = relay_node_exit_batches[i][-1] + service_times[i]
                batch_server_service_start_time[i] = relay_node_exit_batches[i][-1]
        #print(batch_server_exit_times)

        # calculate server exit times for each request
        requests_server_exit_times = (len(arrival_times))*[0]
        req_idx = 0
        for batch_idx in range(len(relay_node_exit_batches)):
            for relay_exit_time in relay_node_exit_batches[batch_idx]:
                requests_server_exit_times[req_idx] = batch_server_exit_times[batch_idx]
                req_idx += 1

        #print(requests_server_exit_times)

        # calculate server queue times
        server_queue_times = (len(arrival_times))*[0]
        curr_idx = 0
        for batch_idx in range(len(batch_server_service_start_time)):
            for relay_exit_time in relay_node_exit_batches[batch_idx]:
                server_queue_times[curr_idx] = batch_server_service_start_time[batch_idx] - relay_node_exit_batches[batch_idx][-1]
                curr_idx += 1

        # calculate server residence times
        server_residence_times = (len(arrival_times)) * [0]
        for i in range(len(arrival_times)):
            server_residence_times[i] = requests_server_exit_times[i] - relay_exit_times[i]


        # calculate end to end times
        end_to_end_times = (len(arrival_times)) * [0]
        for i in range(len(arrival_times)):
            end_to_end_times[i] = requests_server_exit_times[i] - arrival_times[i]

        # calculate metrics
        avg_inter_arrival_time = Sim_math_ops.avg_inter_arrival(arrival_times)
        avg_relay_node_residence_time = Sim_math_ops.average(relay_node_res_times)
        avg_server_queue_time = Sim_math_ops.average(server_queue_times)
        avg_server_service_time = Sim_math_ops.average(service_times)
        avg_server_residence_time = Sim_math_ops.average(server_residence_times)
        avg_end_to_end_time = Sim_math_ops.average(end_to_end_times)

        return [avg_inter_arrival_time, avg_relay_node_residence_time, avg_server_queue_time, avg_server_service_time,
                avg_server_residence_time, avg_end_to_end_time]


m = 1  # repetition of experiments
switch_ia_thrsh = 75
NPIAC = 3
c_thrsh = 3
arrival_times_filepath = r"C:\Users\juanp\OneDrive\Documents\experiments\temp\temp.txt"
service_times_filepath = r"C:\Users\juanp\OneDrive\Documents\experiments\temp\temp2.txt"
service_time_settings = ConstantDistributionSettings(40,service_times_filepath)
isVerbose = False

avg_measured_inter_arrival_times = m * [0]
avg_relay_node_residence_times = m * [0]
avg_server_queue_times = m * [0]
avg_measured_server_service_times = m * [0]
avg_server_residence_times = m * [0]
avg_end_to_end_times = m * [0]
print_all_results = True

for i in range(m):
    metrics = Adaptive.run(switch_ia_thrsh, NPIAC, c_thrsh, arrival_times_filepath,service_time_settings, isVerbose)
    avg_measured_inter_arrival_times[i] = metrics[0]
    avg_relay_node_residence_times[i] = metrics[1]
    avg_server_queue_times[i] = metrics[2]
    avg_measured_server_service_times[i] = metrics[3]
    avg_server_residence_times[i] = metrics[4]
    avg_end_to_end_times[i] = metrics[5]

if print_all_results:
    print("metrics: ")
    print("average measured inter arrival time: " + str(Sim_math_ops.average(avg_measured_inter_arrival_times)))
    print("avg_relay_node_residence_times: " + str(Sim_math_ops.average(avg_relay_node_residence_times)))
    print("avg_server_queue_times: " + str(Sim_math_ops.average(avg_server_queue_times)))
    print("avg_measured_server_service_times: " + str(Sim_math_ops.average(avg_measured_server_service_times)))
    print("avg_server_residence_times: " + str(Sim_math_ops.average(avg_server_residence_times)))
print("avg_end_to_end_times: " + str(Sim_math_ops.average(avg_end_to_end_times)))