# this code simulates an MM1 Queue
# the algorithm used is from Gareth Tribello's youtube video: Simulating the M/M/1 queue
# here is the link to the video: https://www.youtube.com/watch?v=12XbrjiZ1FA&ab_channel=GarethTribello
# This code is different in 3 aspects: First the function to generate exponentialy distributed values is different,
# secondly the average inter arrival time can be other than one, and thirdly the number of requests used in the simulation is variable

from Sim_math_ops import Sim_math_ops
from MultBarDistr import MultBarDistr
from ServiceTimeSettings import *

class A:
    @staticmethod
    def run(arrival_times=[], service_time_distribution=ExponentialDistributionSettings, n=10, avg_service_time=40, avg_inter_arrival_time=50, isVerbose=False):
        service_times = []

        # create the arrival times and service times if arrivals not specified
        if len(arrival_times) == 0:
            arrival_times = n * [0]
            for i in range(1, n):  # the first arrival is taken to happen at time 0
                arrival_times[i] = arrival_times[i - 1] + Sim_math_ops.exp(avg_inter_arrival_time)
            # create the service times
            service_times = n * [0]
            if type(service_time_distribution) == ConstantDistributionSettings:
                for i in range(n):
                    service_times[i] = Sim_math_ops.const(avg_service_time)
            elif type(service_time_distribution) == ExponentialDistributionSettings:
                for i in range(n):
                    service_times[i] = Sim_math_ops.exp(avg_service_time)
            else:
                NameError('Incorrect distribution for Service Time')
        else:
            # create service times if arrivals are given
            service_times = len(arrival_times) * [0]
            if type(service_time_distribution) == ConstantDistributionSettings:
                for i in range(len(service_times)):
                    service_times[i] = Sim_math_ops.const(avg_service_time)
            elif type(service_time_distribution) == ExponentialDistributionSettings:
                for i in range(len(service_times)):
                    service_times[i] = Sim_math_ops.exp(avg_service_time)
            else:
                NameError('Incorrect distribution for Service Time')
        
        n = len(arrival_times)
        
        # for each request, compute the time of entry to the service time, the time of exit from the service time, and the total time spent in the queue
        enter_service_times = n * [0]
        leave_service_times = n * [0]
        queue_times = n * [0]  # the first queue time is zero
        leave_service_times[0] = arrival_times[0] + service_times[0]  # The first request does not have to wait in the queue, it will leave the system as soon as it finished its service time
        for i in range(1, n):
            if leave_service_times[i - 1] < arrival_times[i]:  # the request at index i arrived to the server after the request before it left.
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
m = 1  # number of times the experiment is run

# Settings when n is specified
#n = 10000  # number of requests
#avg_service_time = 40  # average service time
#avg_inter_arrival_time = 100  # average inter arrival time
#arrival_times = MultBarDistr.run(r"C:\Users\juanpablocontreras\Documents\temp\temp.txt",20,10,100,50,"CONSTANT")
#isVerbose = False

max_experiment_time = 5400000
arrival_times_distribution = "POISSON"
arrival_times_filepath = "" #r"C:\Users\juanp\OneDrive\Documents\experiments\temp\temp.txt"
service_times_filepath = "" #r"C:\Users\juanp\OneDrive\Documents\experiments\temp\temp2.txt"
# service_time_distribution = ConstantDistributionSettings(40,r"C:\Users\juanpablocontreras\Documents\temp\st.txt")
service_time_settings = ExponentialDistributionSettings(40,service_times_filepath)
slow_inter_arrival_time = 100   # the low rate inter arrival time
fast_inter_arrival_time = 50    # the high rate inter arrival time
resultspath = r"M:\temp\res.txt"
write_headers = True
isVerbose = False

average_residence_times = m * [0]

#for i in range(m):
#    average_residence_times[i] = A.run(arrival_times=arrivalTimes,service_time_distribution=service_time_distribution, isVerbose=True)

I_values = [500,1000]
I_values.extend(list(range(2500,20000, 2500)))
I_values.extend( list(range(20000,100000,10000)))
I_values.extend( list(range(100000,1000000,100000)))
I_values.extend( list(range(1000000,11000000,1000000)))
for I in I_values:
    # write headers
    if write_headers:
        f = open(resultspath,"w")
        f.write("I_values,")
        f.write("A avg end-to-end")
        f.write("\n")
        f.close()
        write_headers = False

    average_residence_times = m * [0]
    # create the arrival times
    for exp_num in range(m):
        arrival_times = MultBarDistr.run("",max_experiment_time,I,slow_inter_arrival_time,fast_inter_arrival_time,arrival_times_distribution)

        # perform experiment
        average_residence_times[exp_num] = A.run(arrival_times=arrival_times,service_time_distribution=service_time_settings)

    # calculate average end to end time for each NPIAC
    avg_E = Sim_math_ops.average(average_residence_times)

    #write results
    f = open(resultspath, "a")
    f.write(str(I)+",")
    f.write(str(avg_E)+",")
    f.write("\n")
    f.close()
