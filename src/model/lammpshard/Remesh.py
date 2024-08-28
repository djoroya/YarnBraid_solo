
import numpy as np

def remesh_step(traj,r0):
    traj = np.flip(traj, axis=0)
    t = np.cumsum(np.sum(np.diff(traj, axis=0)**2,axis=1)**0.5)
    # add 0
    t = np.insert(t,0,0)
    tnew = np.arange(0, t[-1], r0)

    trajnew = np.array([np.interp(tnew, t, traj[:,i]) for i in range(3)]).T
    return trajnew

def Remesh(trajs):
    r0 = [ np.mean(np.sum(np.diff(traj, axis=0)**2,axis=1)**0.5) 
          for traj in trajs]
    r0 = np.mean(r0)
    trajs_new = [remesh_step(traj,r0) for traj in trajs]
    nlens     = [traj.shape[0] for traj in trajs_new]
    min_len   = np.min(nlens)
    trajs_new = [traj[:min_len,:] for traj in trajs_new]
    trajs_new = [ np.flip(traj, axis=0) for traj in trajs_new]
    trajs     = trajs_new
    return trajs,r0