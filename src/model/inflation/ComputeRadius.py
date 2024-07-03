from tools.calculix.frd.readfrd import readfrd
import numpy as np

def ComputeRadius(params):
    # Debemos calcular el radio de la superficie de cada yarn 
    # despues de la inflacion
    # para eso debemos leer el frd y calcular el radio de cada yarn
    # lo guardamos en params["radius_bot"]
    out = readfrd(params["frd"])
    out = out["data"]
# create xD = x + D1, yD = y + D2, zD = z + D3
    out['xD'] = out['x'] + out['D1']
    out['yD'] = out['y'] + out['D2']
    out['zD'] = out['z'] + out['D3']
    keys_esq = [ ikeys for ikeys in params["nsets"].keys() 
                        if "esq" in ikeys]
    keys_bot = [ ikeys for ikeys in params["nsets"].keys() 
                        if "FACE_BOT" in ikeys]
    keys_sup = [ ikeys for ikeys in params["nsets"].keys() 
                        if "FACE_TOP" in ikeys]

    
    radius_bot = []
    keys_bot_top = keys_bot + keys_sup
    for ikey_bot in keys_bot_top:
        df = out.loc[params["nsets"][ikey_bot]]
        x = df['xD'].values
        y = df['yD'].values
        z = df['zD'].values
        
        x_mu = np.mean(x)
        y_mu = np.mean(y)
        z_mu = np.mean(z)

        x_r = x - x_mu
        y_r = y - y_mu
        z_r = z - z_mu

        distance = np.sqrt(x_r**2 + y_r**2 + z_r**2)
        r_max = np.max(distance)
  
        radius_bot.append(r_max)

    params["yarn_radius"] = np.mean(radius_bot)
    params["yarn_radius_std"] = np.std(radius_bot)


    params["radius_max"] = np.max(np.sqrt(out["xD"]**2 + out["yD"]**2))
    params["radius_min"] = np.min(np.sqrt(out["xD"]**2 + out["yD"]**2))
    
    # compute height
    params["height"] = np.max(out["zD"]) - np.min(out["zD"])
    # Calculamos 