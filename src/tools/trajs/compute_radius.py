import numpy as np

def compute_radius(t1,t2):
    r0 = np.min(np.linalg.norm(t1[:,None,:]-t2[None,:,:],axis=-1))/2
    return r0