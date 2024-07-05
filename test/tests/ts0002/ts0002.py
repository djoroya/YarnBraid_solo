
from model.lammps.default          import default as lmp_default
from model.lsdyna.default          import default as lsdyna_default
from model.lammps.RunLammps         import RunLammps
from model.lsdyna.RunLSdyna  import RunLSdyna

import os
from tools.step.rerun import rerun
from tools.step.deletesim import deletesim
join = os.path.join
def ts0002():
    main_path = ["output"]

    # Run Lammps
    params_lmp = lmp_default()
    print(params_lmp)

    RunLammps(params_lmp,main_path)

    # Run LSdyna

    params_lsdyna = lsdyna_default()
    params_lsdyna['lmp_path']      = params_lmp["simulation_path"]
    params_lsdyna["radius"]        = None # take the radius from the lammps simulation
    params_lsdyna["npoints"]       = 50

    RunLSdyna(params_lsdyna,main_path)

    json_file = join(*(main_path + \
                       [params_lsdyna["simulation_path"]])) + \
                     ".json"

    rerun(json_file,overwrite=True)

    deletesim(json_file)