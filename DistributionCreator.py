#Creates numbers with a certain specified distribution and writes them or appends them to a file.
import numpy as np  # linear algebra
import math
import unittest
import matplotlib.pyplot as plt
from scipy import stats

class DistributionCreator(unittest.TestCase):

    @staticmethod
    #reads scalars from a file as stored by any of the distribution procedures described after this function
    def read(filepath):
        f = open(filepath, 'r')
        lines = f.readlines()
        f.close()
        points = len(lines) * [0]
        idx = 0
        for line in lines:
            points[idx] = float(line.strip())
            idx += 1
        return points

    @staticmethod
    def write_list_of_numbers(list_of_numbers,filepath,append=True):
        f = ''
        if append:
            f = open(filepath,"a")
        else:
            f = open(filepath,"w")
        num_items = len(list_of_numbers)
        for i in range(num_items):
            f.write(str(list_of_numbers[i]))
            if i != num_items-1:
                f.write("\n")
        f.close()
        return


    @staticmethod
    # Creates and writes n scalars that are exponentially distributed
    def exponential(n,mean,filepath,append=True):
        list_of_numbers = n*[0]
        for i in range(n):
            list_of_numbers[i] = -mean * math.log(1 - np.random.uniform(0, 1))
        DistributionCreator.write_list_of_numbers(list_of_numbers,filepath,append)
        return

    @staticmethod
    # Creates and writes n scalars all equal to the constant value
    def constant(n,value,filepath,append=True):
        list_of_numbers = n * [value]
        DistributionCreator.write_list_of_numbers(list_of_numbers,filepath,append)
        return

    @staticmethod
    # Creates and writes n scalars that are the y values of the specified line for x=0,1,2,...,n
    def linear(n,y_intercept,slope, filepath, append=True):
        list_of_numbers = n * [0]
        for i in range(n):
            list_of_numbers[i] = y_intercept + i*slope
        DistributionCreator.write_list_of_numbers(list_of_numbers, filepath, append)
        return


    @staticmethod
    # Creates and writes n scalars that are samples of exponential distributions with means equal to the y values of the specified line for x=0,1,2,...,n
    # The result is in the form sample(exp(mean=y_intercept)), sample(exp(mean=y_intercept + 1*slope)), sample(exp(mean=y_intercept+2*slope)),...,sample(exp(mean=y_intercept+n*slope))
    # this is useful to simulate storage devices with an access time and a write time
    def linear_exponential(n,y_intercept,slope, filepath, append=True):
        list_of_numbers = n * [0]
        for i in range(n):
            list_of_numbers[i] = -(y_intercept + i * slope) * math.log(1 - np.random.uniform(0, 1))
        DistributionCreator.write_list_of_numbers(list_of_numbers, filepath, append)
        return



    def test_exponential(self):
        n = 1000
        mean = 50
        rate_parameter = 1/mean
        filepath = r'C:\Users\juanp\OneDrive\Documents\test\temp\temp.txt'
        DistributionCreator.exponential(n,mean,filepath,False)

        #read the numbers
        points = DistributionCreator.read(filepath)

        #show distribution on histogram
        #plt.hist(points)
        #plt.show()

        #standarize variates
        #for i in range(len(points)):
        #    points[i] = points[i]*(1/mean)

        #calculate goodness of fit
        D,p_value = stats.kstest(points,"expon",args=[0,mean], alternative="less")
        print("D=" + str(D) + ",   p_value=" + str(p_value))

        self.assertTrue(p_value > 0.05)


if __name__ == '__main__':
    unittest.main()