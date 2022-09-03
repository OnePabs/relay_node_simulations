# this code simulates an MM1 Queue
# the algorithm used is from Gareth Tribello's youtube video: Simulating the M/M/1 queue
# here is the link to the video: https://www.youtube.com/watch?v=12XbrjiZ1FA&ab_channel=GarethTribello
# This code is different in 3 aspects: First the function to generate exponentialy distributed values is different,
# secondly the average inter arrival time can be other than one, and thirdly the number of requests used in the simulation is variable

from Sim_math_ops import Sim_math_ops

class MM1QueueSim:
    @staticmethod
    def run(n, avg_service_time, avg_inter_arrival_time, isVerbose):
        # create the service times
        service_times = n * [0]
        for i in range(n):
            service_times[i] = Sim_math_ops.exp(avg_service_time)

        # create the arrival times
        arrival_times = n * [0]
        for i in range(1, n):  # the first arrival is taken to happen at time 0
            arrival_times[i] = arrival_times[i - 1] + Sim_math_ops.exp(avg_inter_arrival_time)

        # for each request, compute the time of entry to the service time, the time of exit from the service time, and the total time spent in the queue
        enter_service_times = n * [0]
        leave_service_times = n * [0]
        queue_times = n * [0]  # the first queue time is zero
        leave_service_times[0] = service_times[
            0]  # The first request does not have to wait in the queue, it will leave the system as soon as it finished its service time
        for i in range(1, n):
            if leave_service_times[i - 1] < arrival_times[
                i]:  # the request at index i arrived to the server after the request before it left.
                enter_service_times[i] = arrival_times[
                    i]  # Request i does not have to wait in the queue. It starts its service time right away
                queue_times[i] = 0
            else:
                enter_service_times[i] = leave_service_times[
                    i - 1]  # Request at I has to wait until request at (i-1) leaves the system in order to start its service time
                queue_times[i] = enter_service_times[i] - arrival_times[i]
            # calculate the time at which request i leaves the system and its service time
            leave_service_times[i] = enter_service_times[i] + service_times[i]

        # calculate residence times
        residence_times = n * [0]
        for i in range(n):
            residence_times[i] = leave_service_times[i] - arrival_times[i]

        # Get the simulation metrics
        measured_avg_inter_arrival_time = Sim_math_ops.avg_inter_arrival(arrival_times)
        measured_avg_service_time = Sim_math_ops.average(service_times)
        average_queue_time = Sim_math_ops.average(queue_times)
        average_residence_time = Sim_math_ops.average(residence_times)

        # print(residence_times)
        if (isVerbose):
            print("average measured inter arrival time: " + str(measured_avg_inter_arrival_time))
            print("average measured service time: " + str(measured_avg_service_time))
            print("average measured queue time: " + str(average_queue_time))
            print("average measured residence time: " + str(average_residence_time))

        return average_residence_time


# Script
# set the variables for the simulation
m = 100  # number of times the experiment is run
n = 10000  # number of requests
avg_service_time = 40  # average service time
avg_inter_arrival_time = 100  # average inter arrival time
isVerbose = False

average_residence_times = m * [0]
for i in range(m):
    average_residence_times[i] = MM1QueueSim.run(n, avg_service_time, avg_inter_arrival_time, isVerbose)

print("average_residence_time: " + str(Sim_math_ops.average(average_residence_times)))
average_residence_time: 198.8661348531755