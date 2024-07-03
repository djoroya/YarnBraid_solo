import numpy as np
import pandas as pd
def df_respan(lsdyna_params):
    
    npoints = lsdyna_params["npoints"]
    df = pd.read_csv(lsdyna_params["lmp_path"]+"data.csv")

    types = np.unique(df["type"])
    df = [df[df["type"]==t] for t in types]
    df = df[:64]


    df = [ df[i].iloc[:npoints,:] for i in range(len(df))]
    df = pd.concat(df)

    # =============================================================================
    types = np.unique(df["type"])
    df = [df[df["type"] == t] for t in types]

    df_np = [d.values[:, 1:] for d in df]
    Nold = df_np[0].shape[0]
    Nnew = 400

    old_span = np.linspace(0, 1, Nold)
    new_span = np.linspace(0, 1, Nnew)

    df_np_interp = [np.array([np.interp(new_span, old_span, d[:, i])
                            for i in range(3)]) for d in df_np]

    df_pandas = []
    for i in range(len(df_np_interp)):
        # types
        types = np.repeat(i+1, Nnew)
        # df pandas [ type, x, y, z]
        df_panda = pd.DataFrame(np.vstack((types, df_np_interp[i])).T, columns=[
                                "type", "x", "y", "z"])
        df_pandas.append(df_panda)
    df = df_pandas

    return df