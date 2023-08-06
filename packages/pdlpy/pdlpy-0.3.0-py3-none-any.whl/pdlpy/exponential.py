from pdlpy.distribution import Distribution
from pdlpy.math import e, log


class Exponential(Distribution):
    """
    Continuous probability distribution of time between events in a Poisson process
    """

    def __init__(self, rate: float):
        """
        Paramters
        rate: the average number of events
        """
        self._rate = rate
        self._mean = rate ** -1
        self._median = log(2) / rate
        self._mode = 0
        self._var = rate ** -2

    def __str__(self):
        return (
            "Exponential("
            f"rate={self._rate:.2f}, "
            f"mean={self._mean:.2f}, "
            f"median={self._median:.2f}, "
            f"mode={self._mode:.2f}, "
            f"var={self._var:.2f}"
            ")"
        )

    def pdf(self, x: float) -> float:
        """
        Probability Density Function

        Paramters
        x: a value of random variable X

        Returns
        the relative likelihood that a value of X would lie in sample space
        """
        return self._rate * e ** (-self._rate * x)

    def cdf(self, x: float) -> float:
        """
        Cumulative Distribution Function

        Parameters
        x: a value of the random variable X

        Returns
        the probability that X will take a value less than or equal to x
        """
        return 1 - e ** (-self._rate * x)
