import datetime
import numpy as np

def path_gen():
    day = datetime.datetime.now().strftime("%Y-%m-%d")
    hour = datetime.datetime.now().strftime("%H-%M-%S")
    rand = np.random.randint(10000,99999)
    return day+"__"+hour+"__"+str(rand)