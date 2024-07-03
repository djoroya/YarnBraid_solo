import os
import pandas as pd
import numpy as np


def build_geo(points_type, out_folder, radius, name):


    main_file = out_folder + '/main.cfile'
    file = open(main_file, 'w')

    lines = """cemptymodel
refcoordsys 0 0.0 0.0 0.0 0.0 0.0 1.0 1.0 0.0 0.0
"""
    file.write(lines)

    # only take the first 50 points of each type

    for index, row in points_type.iterrows():
        # x y z
        lines = 'pnt param  coordsys 1c  {} \t{}\t {}\n'.format(
            row['xu'], row['yu'], row['zu'])
        file.write(lines)

    Nlast = 0
    Nstart = 1
    line_head = """$# =============================================
$#                   Yarn Curves 
$# =============================================     
    """
    file.write(line_head)

    Nlen = len(points_type)
    Nlast += len(points_type)
    # like lines = 'splcur fit  piecewise 10 1v "2--10"'
    lines = 'splcur fit  piecewise {} {}v "{}--{}"\n'.format(
        Nlen, Nstart, Nstart+1, Nlast)

    Nstart = Nlast + 1
    file.write(lines)
# smooth

    line_head = """$# =============================================
$#                   Yarn Curves Smooth
$# =============================================     
    """
    file.write(line_head)

    lines = "cursmooth  0 0.25 0 0  1e\n"
    file.write(lines)


    lines = """ 
circle pntaxis  NPOINTS_VARv 1e 2 0 RADIUS_VAR 0
""".replace('RADIUS_VAR', str(radius)).replace('NPOINTS_VAR', str(Nlen))
    file.write(lines)

    lines = """ 
curbreak  tangentspan preview 2e 120
curbreak  tangentspan apply
"""
    file.write(lines)


    SS1 = Nlen + 4
    SS2 = Nlen + 5
    SS3 = Nlen + 7
    lines = """
line pntpnt  0 0 2 NPOINTS_VARv SS1
line pntpnt  0 0 2 NPOINTS_VARv SS2
line pntpnt  0 0 2 NPOINTS_VARv SS3
""".replace('NPOINTS_VAR', str(Nlen+2)).replace('SS1', str(SS1)).replace('SS2', str(SS2)).replace('SS3', str(SS3))
    file.write(lines)


    lines = """
fillplane 0 0 6e 8 5
fillplane 0 0 7e 10 4
fillplane 0 0 12e 9 3
"""
    file.write(lines)

    lines = """
sweepsld num 3 1f 3 2 1e 0 0 0 2
geomag export visiblestep "OUTFILE_VAR" 1comps
exit
""".replace('OUTFILE_VAR', out_folder + "/" + name + ".step").replace('NPOINTS_VAR', str(Nlen))
    file.write(lines)
    file.close()
    return
