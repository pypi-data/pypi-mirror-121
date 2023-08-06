import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution


class Binomial(Distribution):
    """Binomial distribution class for calculating and
    visualizing a Binomial distribution.

    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring

    """

    def __init__(self, p=0, n=0):
        Distribution.__init__(
            self
        )  # Or use super function as super(Distribution).__init__()

        self.p = p
        self.n = n
        self.mean = self.calculate_mean()

        self.stdev = self.calculate_stdev()

    def calculate_mean(self):
        """Function to calculate the mean from p and n

        Args:
            None

        Returns:
            float: mean of the data set

        """
        return self.n * self.p

    def calculate_stdev(self):
        """Function to calculate the standard deviation from p and n.

        Args:
            None

        Returns:
            float: standard deviation of the data set

        """
        stdev = math.sqrt(self.n * self.p * (1 - self.p))
        return stdev

    def replace_stats_with_data(self):
        """Function to calculate p and n from the data set. The function updates the p and n variables of the object.

        Args:
            None

        Returns:
            float: the p value
            float: the n value

        """
        self.n = len(self.data)
        self.p = self.data.count(1) / self.n
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        return self.p, self.n

    def plot_bar(self):
        """Function to output a histogram of the instance variable data using
        matplotlib pyplot library.

        Args:
            None

        Returns:
            None
        """
        plt.hist(self.data)
        plt.title("Bar Chart")
        plt.xlabel("Events")
        plt.ylabel("Count")

    def pdf(self, k):
        """Probability density function calculator for the binomial distribution.

        Args:
            k (float): point for calculating the probability density function


        Returns:
            float: probability density function output
        """
        combinations = math.factorial(self.n) / (
            math.factorial(self.n - k) * math.factorial(k)
        )
        F = combinations * math.pow(self.p, k) * math.pow(1 - self.p, self.n - k)
        return F

    def plot_bar_pdf(self):
        """Function to plot the pdf of the binomial distribution

        Args:
            None

        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot

        """

        probabilities = []
        range_ = []
        for k in range(0, self.n + 1):
            range_.append(k)
            probability = self.pdf(k)
            probabilities.append(probability)

        plt.bar(range_, probabilities)
        plt.title("Probability Density Function")
        plt.xlabel("K value of probability")
        plt.ylabel("Probabilities")

    def __add__(self, other):
        """Function to add together two Binomial distributions with equal p

        Args:
            other (Binomial): Binomial instance

        Returns:
            Binomial: Binomial distribution

        """

        try:
            assert self.p == other.p, "p values are not equal"
        except AssertionError as error:
            raise

        n_sum = self.n + other.n
        result = Binomial(p=self.p, n=n_sum)
        return result

    def __repr__(self):
        """Function to output the characteristics of the Binomial instance

        Args:
            None

        Returns:
            string: characteristics of the Binomial object

        """

        return (
            f"mean {self.mean}, standard deviation {self.stdev}, p {self.p}, n {self.n}"
        )
