
from IPython.display import HTML, display, clear_output
import numpy as np
import pandas as pd
from datetime import datetime
# timedelta
from datetime import timedelta
init_date = datetime.today().strftime('%Y-%b-%d   |  %H:%M')

def init_table(vars,procesos,df):

    npro = len(procesos)

    procesos = np.array(procesos)
    procesos = procesos.reshape(1,-1)
    reloj    = np.tile("🕔",[1,npro])
    zr       = np.tile("0",[1,npro])
    id       = np.arange(1,npro+1).reshape(1,-1)
    state    = np.tile(15*" ",[1,npro])
    date     = np.tile(15*" ",[1,npro])
    vars_spans = [ np.array([df[ivar].values]) for ivar in vars.keys()]
    # list -> tuple
    vars_spans.insert(0,reloj)
    vars_spans.insert(0,procesos)
    vars_spans.insert(0,id)
    vars_spans.append(state)
    vars_spans.append(date)
    vars_spans.append(zr)
    vars_spans = np.array(vars_spans)
    vars_spans = [ var.T for var in vars_spans]
    data = np.hstack(vars_spans)

    procesos = pd.DataFrame(data,columns=["ID","name","Status"] +
                                         list(vars.keys()) + 
                                         ["Loading","Date","time"])
    return procesos
# =========================================================
def mostrar_tabla(procesos,i,j,nsteps,times):

    total = 8

    nblock = int(total * ((j + 1) / nsteps))

    nblock = min(nblock,total)

    block = nblock * "▉"

    nspace = total - nblock
    space = (nspace) * " "
    string = "(" + str(j + 1) + "/" + str(nsteps) + ") "
    # align="left"
    full = f'<font color="green">{string}</font>{block + space}'
    string = "<div style='text-align: left;'>" + full + "</div>"
    procesos["Loading"][i] = string
    # yyyy-mm-dd hh:mm:ss
    procesos["Date"][i] = datetime.today().strftime('%Y-%b-%d   |  %H:%M')
    html = procesos.to_html(escape=False,index=False)
    # align="center"
    #html = html.replace('<th>','<th style="text-align: right;">')
    # put vertical lines in table
    html = html.replace('<td>','<td style="border: 1px solid black;">')
    # put horizontal lines in table
    html = html.replace('<th>','<th style="border: 1px solid black;">')
    # center titles
    html = html.replace('<th>','<th style="text-align: center;">')
    clear_output(wait=True)
    npro = len(procesos)
    current_date = datetime.today().strftime('%Y-%b-%d   |  %H:%M')
    head = "<h3>Parametrization ("+str(i)+\
                "/"+str(npro)+")    [<span style='color: green'>"+\
                    init_date+"</span>] - [<span style='color:green'>"+current_date +"</span>]  </h3>"
    seconds = "<h4>Elapsed time: "+str(round(np.sum(times),2))+" s</h4>"
    # hours, minutes, seconds
    et = np.sum(times) * npro / (i+1)
    et_hours = et // 3600
    et_minutes = (et % 3600) // 60
    et_seconds = (et % 3600) % 60
    estimated = "<h4>Estimated time: "+str(int(et_hours))+" h "+\
                str(int(et_minutes))+" min "+\
                str(int(et_seconds))+" sec</h4>"
    
    date_estimated = datetime.today() + timedelta(seconds=et)
    datetime_estimated = date_estimated.strftime('%Y-%b-%d   |  %H:%M')
    estimated = "<h4>Estimated end: "+datetime_estimated+"</h4>"
    html = head + seconds + estimated + html
    display(HTML(html))

def dataframize(vars):
    values = [ vars[ivar]["span"] for ivar in vars.keys()]
    ms = np.meshgrid(*values)
    flat = [m.flatten() for m in ms]
    points = np.vstack(flat).T

    df = pd.DataFrame(points, columns=vars.keys())
    # set type 
    for ivar in vars.keys():
        df[ivar] = df[ivar].astype(type(vars[ivar]["span"][0]))
    return df

def setvalue(params,path,value):
    
    try:
        to_change = params
        for ip in path[:-1]:
            to_change = to_change[ip]
        to_change[path[-1]] = value
    except:
        raise Exception("Error in setvalue, \n Error in path: "+str(path))