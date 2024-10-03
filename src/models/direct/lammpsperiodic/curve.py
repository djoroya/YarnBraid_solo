import numpy as np
from models.direct.lammpsperiodic.Remesh import Remesh

sign_smooth = lambda x,eta: 2*(1/(1+np.exp(-eta*x)) - 0.5)

def spiral_tg(t, phase, rs, h, sign=True):

  phi0 = 1/32
  x = rs*np.cos(2*np.pi*(t+phase + phi0))
  y = rs*np.sin(2*np.pi*(t+phase + phi0))
  z = h*t

  if sign:
      sign_value = 1
  else:
      sign_value = -1
   # 0.25*r_hilo*np.cos(2*np.pi*s_span)
  eta = 4
  amplitude = sign_value*0.15*rs*sign_smooth(np.cos(4*2*np.pi*(t+phase)), eta)

  u = np.array([np.cos(2*np.pi*(t+phase)), -np.sin(2*np.pi*(t+phase))])
  un = u/(np.linalg.norm(u))
  x = x - amplitude*un[0]
  y = y + amplitude*un[1]

  v = np.array([x, y, z])
  x, y, z = v

  if sign:
    x, y = y, x

  return x,y,z

# ==============================================================================


def curve(params):
    
    h               = params['h']
    Npoints         = params['Npoints']
    Nhilos__central = params['hilo_central']
    r_hilo          = params['r_hilo']
    n_hilos         = params['nhilos']
    len_periodic    = params['len_periodic']
    n = 8
    t_span = np.linspace(0, len_periodic, Npoints)  #  4/8 1/8

    #rs = 0.35*(2*r_hilo/(np.sqrt(2)))/np.sqrt(1-np.cos(2*np.pi/n))
    rs = r_hilo

    dt = np.diff(t_span)[0]

    sign   = [True, False]
    uphase = [0, 1/16]
    trajs  = []

    min_step = 5e-3
    #min_step = 0.5
    for j, isign in enumerate(sign):
        for iter in range(1, n+1):
            phase = (iter - 1)/n + uphase[j]
            for k,nn in enumerate(np.linspace(-1, 1, n_hilos)):

                traj = []
                phase_nn = phase + (1/32)*nn*0.5
                if isign:
                    rs_nn = rs + min_step*rs*nn 
                else:
                    rs_nn = rs - min_step*rs*nn
                for t in t_span:
                    x, y, z = spiral_tg(t-k*dt      , 
                                        phase_nn    , 
                                        rs_nn       ,
                                        h           ,
                                        sign=isign)
                    traj.append([x, y, z])
                traj = np.array(traj)
                trajs.append(traj)

    # Longitud media de los hilos
    def length(traj):
        L = 0
        for i in range(traj.shape[0]-1):
            L += np.linalg.norm(traj[i+1] - traj[i])
        return L
    
    L = [length(traj) for traj in trajs]
    params["L_hilo"] = np.mean(L)
    # Hilos centrales

    # Medir radio interno
    radius_trajs = [ np.sqrt(traj[0,0]**2 + traj[0,1]**2) for traj in trajs]
    radius_trajs_min = np.min(radius_trajs)
    radius_trajs_max = np.max(radius_trajs)
    grosor = radius_trajs_max - radius_trajs_min
    params["r_mean"] = 0.5*(radius_trajs_max + radius_trajs_min)
    if Nhilos__central == 1:
        traj = [ (0, 0, h*t) for t in t_span]
        traj = np.array(traj)
        trajs.append(traj)
    elif Nhilos__central > 1:

        def curva(t,r,h):
            x = r*np.cos(2*np.pi*t)
            y = r*np.sin(2*np.pi*t)
            z = (np.cos(2*np.pi*t)+1)/2*h
            return x,y,z

        t = np.linspace(0,1/8,100)
        x,y,z = curva(t,r=rs,h=h/2)
        length = np.sum(np.sqrt(np.diff(x)**2+np.diff(y)**2+np.diff(z)**2))
        nhilos = params["nhilos"]
        dist_hilos = params["dist_factor"]*length/(8*nhilos)

        for i in range(Nhilos__central):

            if params["external_hilos"]:
                if i<Nhilos__central//2:
                    rh = radius_trajs_min - 0.5*grosor
                else:
                    rh = radius_trajs_max + 0.5*grosor
                w = 4
            else:
                rh = radius_trajs_min - 0.5*grosor
                w = 2

            ix = rh*np.cos(w*np.pi*i/Nhilos__central)
            iy = rh*np.sin(w*np.pi*i/Nhilos__central)

            traj = [ (ix, iy, h*t) for t in t_span]
            traj = np.array(traj)
            trajs.append(traj)
    

    
    # Remesh
    if params["Remesh"]:
        trajs,r0 = Remesh(trajs)
        params["Npoints"] = trajs[0].shape[0]
        params["r0"]    = r0


    trajs = np.array(trajs)
    params["trajs"] = trajs


    return params