import math
import statistics
from typing import List, NoReturn

from .general import Distribution


class Gaussian(Distribution):
    def __init__(self, mean=0., stdev=1.):
        """Gaussian distribution class."""
        super().__init__(mean, stdev)

    def __add__(self, other) -> 'Gaussian':
        """Method to add together two Gaussian distributions.

        Args:
            other (Gaussian): other Gaussian distribution.

        Returns:
            Gaussian: Gaussian distribution.
        """
        total = Gaussian()
        total.set_mean(self.mean + other.mean)
        total.set_stdev(math.sqrt(self.stdev ** 2 + other.stdev ** 2))
        return total

    def __repr__(self) -> str:
        """Method to print the characteristics of the Gaussian distribution.

        Returns:
            str: characteristics of the Gaussian.
        """
        return f"mean {self.mean}, standard deviation {self.stdev}"

    def calculate_mean(self) -> float:
        """Method to calculate the mean value of the distribution.

        Returns:
            float: The mean value of the distribution.
        """
        new_mean = float(statistics.mean(self.data))
        self.set_mean(new_mean)
        return new_mean

    def calculate_stdev(self) -> float:
        """Method to calculate the standard deviation value
        of the distribution.

        Returns:
            float: The standard deviation value of the distribution.
        """
        new_stdev = float(statistics.stdev(self.data))
        self.set_stdev(new_stdev)
        return new_stdev

    def pdf(self, x: float) -> float:
        """Probability density function.

        Args:
            x (float): Point for calculating the probability density function.

        Returns:
            float: Probability density.
        """
        return (1.0 / (self.stdev * math.sqrt(2 * math.pi))) \
               * math.exp(-0.5 * ((x - self.mean) / self.stdev) ** 2)

    def plot(self) -> NoReturn:  # TODO: implement with matplotlib
        """Plotting histogram.

        Returns:
            NoReturn
        """
        raise NotImplementedError

    def plot_pdf(self, n_spaces=50) -> (List[float], List[float]):
        # TODO: implement with matplotlib
        """Plotting probability density function.

        Args:
            n_spaces (int): Number of plotted points.

        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
        """
        raise NotImplementedError
