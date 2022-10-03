from keras import models
from common.Distributions import *
from common.Sim_math_ops import *


class Predictive:
    @staticmethod
    def run(n, t, model_filepath, arrivals_distribution=Poisson(50), service_time_distribution=Exponential(40)):
        # currently uses 50 previous inter arrivals put into 5 input nodes to predict which technique to use
        if n < 51:
            print("not enough data")
            exit()

        # create arrival times
        arrival_times = arrivals_distribution.create(n)
        # arrival_times.extend([2960, 2970, 2980, 2990])

        # calculate 5 input nodes for all predictions
        # I need the first 51 requests to get the first 50 inter arrival times to make the first prediction. Then there
        # is one prediction per request. That prediction will take the last 50 inter arrival times using the last
        # 51 requests.
        num_requests_per_prediction = 51    # to get 50 inter arrival times
        number_of_ia_per_input_node = 10    # 10 inter arrivals
        five_node_inputs = []   # there should be n-51 5 node input sets
        curr_avg = 0
        for i in range(num_requests_per_prediction, len(arrival_times)):
            # get the input nodes needed to make a prediction after the ith request arrived
            curr_node_inputs = []
            for k in range(0,
                           num_requests_per_prediction - number_of_ia_per_input_node,
                           number_of_ia_per_input_node):
                start_idx = i - num_requests_per_prediction + k
                end_idx = i - num_requests_per_prediction + k + number_of_ia_per_input_node
                # print("i: " + str(i) + ", k: " + str(k) + ", start: " + str(start_idx) + ", end: " + str(end_idx))
                curr_avg = Sim_math_ops.avg_inter_arrival(arrival_times[start_idx:end_idx+1])  # +1 because inclusive
                curr_node_inputs.append(curr_avg)
            five_node_inputs.append(curr_node_inputs)
        # print(five_node_inputs)

        # calculate relay node exit times
        relay_node_exit_times = len(arrival_times) * [0]
        batches = []
        # batches = [[[arr1,...,arr3], relay_exit, st, server_exit], ...,[[arr1,...,arr3], relay_exit, st, server_exit]]
        # the first 51 (num_requests_per_prediction) use technique A
        for i in range(num_requests_per_prediction):
            batches.append([[arrival_times[i]], arrival_times[i]])
        # after the first 51 (num_requests_per_prediction) make predictions
        # load model
        model = models.load_model(model_filepath)
        # make all predictions
        predictions = model.predict(five_node_inputs)
        #print(predictions)
        # use predictions to simulate relay node exit times and create batches
        curr_batch = []
        for i in range(num_requests_per_prediction, len(arrival_times)):
            if predictions[i-num_requests_per_prediction] < 0.5:
                # use technique A
                if len(curr_batch) > 0:
                    # there is a batch that has to be sent to the server
                    # add this request to the current batch and send batch to server
                    curr_batch[0].append(arrival_times[i])  # add arrival time to the batch's list of arrivals
                    curr_batch.append(arrival_times[i])     # set relay node exit time as the arrival of this last req
                    batches.append(curr_batch)              # append current batch to list of batches (i.e. send to server)
                    curr_batch = []                         # reset current batch placeholder
                else:
                    # there is NO batch that is currently being built
                    # add request as its own to the list of batches
                    batches.append([[arrival_times[i]], arrival_times[i]])
            else:
                # use technique C
                if len(curr_batch) > 0:
                    # there is a batch currently being built
                    # add this request to the current batch
                    curr_batch[0].append(arrival_times[i])  # add arrival time to the batch's list of arrivals
                    if len(curr_batch[0]) >= t:
                        # send the batch to server
                        curr_batch.append(arrival_times[i])  # set relay node exit time as the arrival of this last req
                        batches.append(curr_batch)  # append current batch to list of batches (i.e. send to server)
                        curr_batch = []  # reset current batch placeholder
                else:
                    # No batch is currently being built
                    # create a new batch
                    curr_batch.append([arrival_times[i]])
                if (i+1)==len(arrival_times) and len(curr_batch) > 0:
                    # last batch might not be completed
                    # send to server anyway
                    curr_batch.append(arrival_times[i])  # set relay node exit time as the arrival of this last req
                    batches.append(curr_batch)  # append current batch to list of batches (i.e. send to server)
                    curr_batch = []  # reset current batch placeholder

        # create service times
        service_times = service_time_distribution.create(len(batches))
        # copy service times to batches
        for i in range(len(service_times)):
            batches[i].append(service_times[i])

        # calculate server exit times
        # batches = [[[arr1,...,arr3], relay_exit, st, server_exit], ...,[[arr1,...,arr3], relay_exit, st, server_exit]]
        # the first exit time is just the batch arrival time plus the batch service time
        cur_batch_exit_time = batches[0][1] + batches[0][2]
        batches[0].append(cur_batch_exit_time)
        for i in range(1, (len(service_times))):
            if batches[i][1] < batches[i-1][3]:
                # queue. start when the previous batch has been serviced
                cur_batch_exit_time = batches[i - 1][3] + batches[i][2]

            else:
                # no queue.
                cur_batch_exit_time = batches[i][1] + batches[i][2]
            batches[i].append(cur_batch_exit_time)

        # print(batches)

        # calculate end to end times
        # flatten batches to get exit times
        end_to_end_times = len(arrival_times)*[0]
        req_idx = 0
        for i in range(len(batches)):
            cur_batch = batches[i]
            for k in range(len(cur_batch[0])):
                end_to_end_times[req_idx] = cur_batch[3] - arrival_times[req_idx]
                req_idx += 1

        E = Sim_math_ops.average(end_to_end_times)
        return E





