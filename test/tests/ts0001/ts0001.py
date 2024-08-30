
from models.direct.lammpshard.default          import default
from models.direct.lammpshard.RunLammps         import RunLammps

import os
from tools.step.rerun import rerun
from tools.step.deletesim import deletesim
join = os.path.join
def ts0001():
    main_path = ["output"]
    params_lmp = default()
    print(params_lmp)

    RunLammps(params_lmp,main_path)

    

    json_file = join(*(main_path + \
                       [params_lmp["simulation_path"]])) + \
                     ".json"


    rerun(json_file,overwrite=True)

    deletesim(json_file)