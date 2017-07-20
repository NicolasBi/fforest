from typing import Iterable, Tuple, Callable, Sized

from fforest.src.vrac.maths.norms import euclidean
import numpy as np


class HyperSphere:
    """ An HyperSphere, or n-Sphere is a mathematical generalization of the ordinary sphere in spaces of arbitrary
    dimension.

    Inspirations :
        https://en.wikipedia.org/wiki/N-sphere
        http://www.sciencedirect.com/science/article/pii/S0019995862906411

    Attributes :
        - center: np.array[float]
        - dimension: int
        - radius: float
        - norm: Callable, The norm used to compute distances. Default: euclidean
    """
    def __init__(self, center, radius: float, norm: Callable = euclidean):
        self.center = np.array(center)
        self.dimension = len(center)
        self.radius = radius
        self.norm = norm

    def __contains__(self, item):
        """
            Example :
            >>> sphere = HyperSphere(center=(1, 2), radius=1)
            >>> vector = (0, 3)
            >>> vector in sphere
            False
            >>> vector = (0, 2)
            >>> vector in sphere
            True
        """
        self._assert_dimension(item)
        return self.norm(np.array(item) - self.center) <= self.radius

    def _assert_dimension(self, instance):
        assert self.dimension == len(instance)


def hypersphere():
    pass


if __name__ == "__main__":
    pass
