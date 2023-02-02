from datetime import datetime
from pprint import pprint
import numpy as np
import random
import json
import math
import sys

# ******************************************************************************************************************** #
def fileToList(filename: str):
    with open(filename) as f:
        lines = f.read().splitlines()
        for l in lines:
            size = int(l[2:4])

            i = str(l).find('[')
            j = str(l).find(']') + 1
            l = l[i:j]
            l = json.loads(l)
            l = np.array(l).reshape(size, size)

            yield size, l.tolist()