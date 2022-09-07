# classes that store the service time settings depending on the distribution

class ConstantDistributionSettings:
    def __init__(self, const, filepath):
        self.const = const
        self.filepath = filepath


class ExponentialDistributionSettings:
    def __init__(self,mean, filepath):
        self.mean = mean
        self.filepath = filepath


class PoissonDistributionSettings:
    def __init__(self,mean, filepath):
        self.mean = mean
        self.filepath = filepath


class LinearDistributionSettings:
    def __init__(self,y_intercept,slope, filepath):
        self.y_intercept = y_intercept
        self.slope = slope
        self.filepath = filepath



class LinearExponentialDistributionSettings:
    def __init__(self,y_intercept,slope, filepath):
        self.y_intercept = y_intercept
        self.slope = slope
        self.filepath = filepath


