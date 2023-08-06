import math
from typing import NoReturn, Tuple

from .general import Distribution


class Binomial(Distribution):
    def __init__(self, prob=.5, size=20):
        """Binomial distribution class for calculating and
        visualizing a Binomial distribution.

        Attributes:
            mean (float): Representing the mean value of the distribution.
            stdev (float): Representing the standard deviation
                of the distribution.
            data_list (list of floats): A list of floats to be extracted
                from the data file.
            p (float): Representing the probability of an event occurring.
            n (int): The total number of trials.
        """
        self.p = None
        self.set_p(prob)

        self.n = None
        self.set_n(size)

        self.calculate_mean()
        self.calculate_stdev()

    def set_p(self, new_value: float) -> NoReturn:
        """Mutator method realizes encapsulation of p attribute.
        'p' stands for 'probability'.

        Args:
            new_value (float): New value of p attribute.

        Returns:
            NoReturn
        """
        self.p = new_value

    def get_p(self) -> float:
        """Accessor method realizes encapsulation of p attribute.
        'p' stands for 'probability'.

        Returns:
            float: The probability of an event occurring.
        """
        return self.p

    def set_n(self, new_value: int) -> NoReturn:
        """Mutator method realizes encapsulation of n attribute.
        'n' stands for total number of trials.

        Args:
            new_value (float): New value of n attribute.

        Returns:
            NoReturn
        """
        self.n = new_value

    def get_n(self) -> int:
        """Accessor method realizes encapsulation of n attribute.
        'n' stands for total number of trials.

        Returns:
            int: The total number of trials.
        """
        return self.n

    def calculate_mean(self) -> float:
        """Function to calculate the mean from p and n.

        Args:
            None

        Returns:
            float: mean of the data set.
        """
        mean = self.get_p() * self.get_n()
        self.set_mean(mean)
        return mean

    def calculate_stdev(self) -> float:
        """Function to calculate the standard deviation from p and n.

        Args:
            None

        Returns:
            float: standard deviation of the data set.
        """
        variance = self.get_n() * self.get_p() * (1 - self.get_p())
        stdev = math.sqrt(variance)
        self.set_stdev(stdev)
        return stdev

    def replace_stats_with_data(self) -> Tuple[float, int]:
        """Function to calculate p and n from the data set

        Args:
            None

        Returns:
            float: the p value
            float: the n value
        """
        if len(self.data) > 0:
            self.set_n(len(self.data))
            self.set_p(len([k for k in self.data if k > 0]) / len(self.data))
            self.calculate_mean()
            self.calculate_stdev()
            return self.get_p(), self.get_n()
        else:
            raise Exception("The data set is empty.")

    def plot(self) -> NoReturn:  # TODO: implement with matplotlib barplot
        """Function to output a histogram of the instance variable data using
        matplotlib pyplot library.

        Args:
            None

        Returns:
            None
        """
        raise NotImplementedError

    def pdf(self, k) -> float:
        """Probability density function calculator
         for the gaussian distribution.

        Args:
            k (float): point for calculating the probability density function.

        Returns:
            float: probability density function output.
        """
        likelihood = (math.factorial(int(self.get_n())) /
                      (math.factorial(int(k))
                      * math.factorial(int(self.get_n() - k)))) \
                     * (self.get_p()**k * (1-self.get_p())**(self.get_n() - k))
        return likelihood

    def plot_pdf(self) -> NoReturn:  # TODO: implement with matplotlib barplot
        """Function to plot the pdf of the binomial distribution

        Args:
            None

        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
        """
        raise NotImplementedError

    def __add__(self, other: 'Binomial') -> 'Binomial':
        """Function to add together two Binomial distributions with equal p.

        Args:
            other (Binomial): Binomial instance.

        Returns:
            Binomial: Binomial distribution.
        """
        try:
            assert self.get_p() == other.get_p(), 'p values are not equal'
        except AssertionError as error:
            raise error

        total = Binomial()
        total.set_p(self.get_p())
        total.set_n(self.get_n() + other.get_n())
        total.calculate_mean()
        total.calculate_stdev()
        return total

    def __repr__(self) -> str:
        """Function to output the characteristics of the Binomial instance

        Args:
            None

        Returns:
            string: characteristics of the Gaussian
        """
        return f"""mean {self.get_mean()}, 
        standard deviation {self.get_stdev()}, 
        p {self.get_p()}, n {self.get_n()}"""
