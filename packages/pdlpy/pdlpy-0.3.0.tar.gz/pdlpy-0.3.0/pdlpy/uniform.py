from pdlpy.distribution import Distribution


class Uniform(Distribution):
    """
    Continuous distribution of a random variable X in interval [a; b] where any value of X has an equal probability
    """

    def __init__(self, a: float, b: float):
        """
        Paramters
        a: the minimum value of X
        b: the maximum value of X
        """
        self._a = a
        self._b = b
        self._mean = (a + b) / 2
        self._median = (a + b) / 2
        self._mode = (a + b) / 2
        self._var = (b - a) ** 2 / 12

    def __str__(self):
        return (
            "Uniform("
            f"a={self._a:.2f}, "
            f"b={self._b:.2f}, "
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
        return 1 / (self._b - self._a)

    def cdf(self, x: float) -> float:
        """
        Cumulative Distribution Function

        Parameters
        x: a value of the random variable X

        Returns
        the probability that X will take a value less than or equal to x
        """
        if x <= self._a:
            return 0.0
        elif x >= self._b:
            return 1.0
        else:
            return (x - self._a) / (self._b - self._a)
