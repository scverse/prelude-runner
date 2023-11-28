import random
from contextlib import suppress

random.seed(0)

with suppress(Exception):
    from numpy.random import seed

    seed(0)

with suppress(Exception):
    # https://pytorch.org/docs/stable/notes/randomness.html
    import torch

    torch.use_deterministic_algorithms(True)
    torch.manual_seed(0)
