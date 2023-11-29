import random
from contextlib import suppress

random.seed(0)

with suppress(Exception):
    from numpy.random import seed

    seed(0)  # noqa: NPY002
