from tools.calculix.read_dat import read_dat

def ComputeDenier(params,nhilos):
    
    factor        = params["r_hebra"]/params["yarn_radius"]

    r = read_dat(params["output_folder"] + "/init.dat")
    #find the volume 
    dat = [ ir for ir in r if ir["name"] == "volume" ][0]
    volume = dat["df"]["volume"].sum()*factor**3 #mm^3 
    height = params["height"]*factor # mm

    rho = params["rho"] # g/mm^3
    lineal_density = volume*rho/height #  g/mm
    denier = lineal_density*9e6 # denier
    params["linear_density"] = lineal_density
    params["denier"] = denier

    params["denier_per_filament"] = params["denier"]/(16*nhilos)
    params["linear_density_per_filament"] = params["linear_density"]/(16*nhilos)
    params["volume"] = volume