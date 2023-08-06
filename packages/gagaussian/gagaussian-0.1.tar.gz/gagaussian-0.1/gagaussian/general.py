from abc import ABC, abstractmethod
from typing import NoReturn


class DistributionInterface(ABC):
    @abstractmethod
    def __init__(self, mean: float, stdev: float, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def __add__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError

    @abstractmethod
    def read(self, file: str) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def calculate_mean(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def calculate_stdev(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def pdf(self, *args, **kwargs) -> float:
        raise NotImplementedError

    @abstractmethod
    def plot(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def plot_pdf(self, *args, **kwargs):
        raise NotImplementedError


class Distribution(DistributionInterface, ABC):
    def __init__(self, mean=0., stdev=1., *args, **kwargs):
        """General distribution parent class.

        Args:
            mean (float): The mean value of the distribution.
            stdev (float): The standard deviation of the distribution.
        """
        self.mean = None
        self.set_mean(mean)

        self.stdev = None
        self.set_stdev(stdev)

        self.data = []

    def set_mean(self, new_value: float) -> NoReturn:
        """Mutator method realizes encapsulation of mean attribute.

        Args:
            new_value (float): New value of mean attribute.

        Returns:
            NoReturn
        """
        self.mean = new_value

    def get_mean(self) -> float:
        """Accessor method realizes encapsulation of mean attribute.

        Returns:
            float: The mean value of the distribution.
        """
        return self.mean

    def set_stdev(self, new_value: float) -> NoReturn:
        """Mutator method realizes encapsulation of stdev attribute.

        Args:
            new_value (float): New value of stdev attribute.

        Returns:
            NoReturn
        """
        self.stdev = new_value

    def get_stdev(self) -> float:
        """Accessor method realizes encapsulation of stdev attribute.

        Returns:
            float: The stdev value of the distribution.
        """
        return self.stdev

    def read(self, file_name: str) -> NoReturn:
        """Method to read data from a text file.

        Args:
            file_name (str): Name of a file to read.

        Returns:
            NoReturn
        """
        data = []

        with open(file_name) as file:
            while line := file.readline():
                line = int(line.rstrip())
                data.append(line)

        self.data = data
