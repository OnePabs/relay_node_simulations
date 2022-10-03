from common.Sim_math_ops import Sim_math_ops


class Distribution:
    def __init__(self, name="GENERAL"):
        self.name = name

    def create(self, data, write_to_file=False, filepath="", append=False):
        if write_to_file:
            Distribution.write_list_of_numbers(list_of_numbers=data, filepath=filepath, append=append)
            return data
        else:
            return data

    @staticmethod
    def write_list_of_numbers(list_of_numbers, filepath, append=False):
        #print("Parent Distribution write_list_of_numbers filepath = " + filepath)
        f = ''
        if append:
            f = open(filepath, "a")
            f.write("\n")
        else:
            f = open(filepath, "w")
        num_items = len(list_of_numbers)
        for i in range(num_items):
            f.write(str(list_of_numbers[i]))
            if i != num_items - 1:
                f.write("\n")
        f.close()
        return


class Constant(Distribution):
    def __init__(self, constant):
        Distribution("CONSTANT")
        self.constant = constant

    def change_settings(self, constant):
        self.constant = constant
        return

    def create(self, n, write_to_file=False, filepath="", append=False):
        data = n*[self.constant]
        return super().create(data, write_to_file, filepath, append)


class ConstantRunningTotal(Distribution):
    def __init__(self, constant, start_point=0):
        Distribution("CONSTANTRUNNING")
        self.constant = constant
        self.start_point = start_point

    def change_settings(self, constant, start_point=0):
        self.constant = constant
        self.start_point = start_point
        return

    def create(self, n, write_to_file=False, filepath="", append=False):
        data = n * [0]
        data[0] = self.start_point
        for i in range(1,n):
            data[i] = data[i-1] + self.constant
        return super().create(data, write_to_file, filepath, append)


class Exponential(Distribution):
    def __init__(self, mean):
        self.mean = mean

    def change_settings(self, mean):
        self.mean = mean
        return

    def create(self, n, write_to_file=False, filepath="", append=False):
        data = n*[0]
        for i in range(n):
            data[i] = Sim_math_ops.exp(self.mean)
        return super().create(data, write_to_file, filepath, append)


class Poisson(Distribution):
    def __init__(self, mean, start_point=0):
        self.mean = mean
        self.start_point = start_point
        return

    def change_settings(self, mean, start_point=0):
        self.mean = mean
        self.start_point = start_point
        return

    def create(self, n, write_to_file=False, filepath="", append=False):
        data = n * [0]
        if self.start_point > 0:
            data[0] = Sim_math_ops.exp(self.start_point)
        for i in range(1, n):
            data[i] = data[i-1] + Sim_math_ops.exp(self.mean)
        return super().create(data, write_to_file, filepath, append)


class MultipleBarsConstant(Distribution):
    # __--__--__--__--
    def __init__(self, first_part_intervals, second_part_intervals, n_per_cycle, load_factor):
        # high: the value of the inter arrival times for the high bar
        # first_part_intervals: the value of the intervals for the first part until n_per_cycle*load_factor
        # second_part_ia: the value of the intervals for the second part from n_per_cycle*load_factor to n_per_cycle
        # nPerCycle: the number of points in one cycle. where one cycle is one repeating pattern of bars i.e __--
        # load_factor: the fraction of number of points at low value and all points in one cycle. = n_low/(n_low+n_high)
        self.first_part_intervals = first_part_intervals
        self.second_part_intervals = second_part_intervals
        self.n_per_cycle = n_per_cycle
        self.load_factor = load_factor
        return

    def change_settings(self, first_part_intervals, second_part_intervals, n_per_cycle, load_factor):
        self.first_part_intervals = first_part_intervals
        self.second_part_intervals = second_part_intervals
        self.n_per_cycle = n_per_cycle
        self.load_factor = load_factor
        return

    def create(self, n, write_to_file=False, filepath="", append=False):
        # n is the number of points to create
        data = n * [0]
        for i in range(n):
            if i%self.n_per_cycle < self.load_factor*self.n_per_cycle:
                # use low value
                data[i] = self.first_part_intervals
            else:
                data[i] = self.second_part_intervals
        return super().create(data, write_to_file, filepath, append)


class MultipleBarsExponential(Distribution):
    def __init__(self, first_part_intervals, second_part_intervals, n_per_cycle, load_factor):
        # high: the value of the inter arrival times for the high bar
        # first_part_intervals: the value of the intervals for the first part until n_per_cycle*load_factor
        # second_part_ia: the value of the intervals for the second part from n_per_cycle*load_factor to n_per_cycle
        # nPerCycle: the number of points in one cycle. where one cycle is one repeating pattern of bars i.e __--
        # load_factor: the fraction of number of points at low value and all points in one cycle. = n_low/(n_low+n_high)
        self.first_part_intervals = first_part_intervals
        self.second_part_intervals = second_part_intervals
        self.n_per_cycle = n_per_cycle
        self.load_factor = load_factor
        return

    def change_settings(self, first_part_intervals, second_part_intervals, n_per_cycle, load_factor):
        self.first_part_intervals = first_part_intervals
        self.second_part_intervals = second_part_intervals
        self.n_per_cycle = n_per_cycle
        self.load_factor = load_factor
        return

    def create(self, n, write_to_file=False, filepath="", append=False):
        # n is the number of points to create
        data = n * [0]
        comp = int(round(self.load_factor * self.n_per_cycle))
        for i in range(n):
            if i % self.n_per_cycle < comp:
                # use low value
                data[i] = Sim_math_ops.exp(self.first_part_intervals)
            else:
                data[i] = Sim_math_ops.exp(self.second_part_intervals)
        return super().create(data=data, write_to_file=write_to_file, filepath=filepath, append=append)



class MultipleBarsPoisson(Distribution):
    # __--__--__--__--
    def __init__(self, first_part_intervals, second_part_intervals, n_per_cycle, load_factor):
        # high: the value of the inter arrival times for the high bar
        # first_part_intervals: the value of the intervals for the first part until n_per_cycle*load_factor
        # second_part_ia: the value of the intervals for the second part from n_per_cycle*load_factor to n_per_cycle
        # nPerCycle: the number of points in one cycle. where one cycle is one repeating pattern of bars i.e __--
        # load_factor: the fraction of number of points at low value and all points in one cycle. = n_low/(n_low+n_high)
        self.first_part_intervals = first_part_intervals
        self.second_part_intervals = second_part_intervals
        self.n_per_cycle = n_per_cycle
        self.load_factor = load_factor
        return

    def change_settings(self, first_part_intervals, second_part_intervals, n_per_cycle, load_factor):
        self.first_part_intervals = first_part_intervals
        self.second_part_intervals = second_part_intervals
        self.n_per_cycle = n_per_cycle
        self.load_factor = load_factor
        return

    def create(self, n, write_to_file=False, filepath="", append=False):
        # n is the number of points to create
        data = n * [0]
        comp = int(round(self.load_factor * self.n_per_cycle))
        for i in range(1, n):
            if i % self.n_per_cycle < comp:
                # use low value
                data[i] = data[i-1] + Sim_math_ops.exp(self.first_part_intervals)
            else:
                data[i] = data[i-1] + Sim_math_ops.exp(self.second_part_intervals)
        return super().create(data=data, write_to_file=write_to_file, filepath=filepath, append=append)




