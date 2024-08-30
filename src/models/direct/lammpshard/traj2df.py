import pandas as pd

def traj2df(trajs):
    # deactivate warning
    df_list = []
    for i in range(len(trajs)):
        df_i = pd.DataFrame(trajs[i], columns=["xu", "yu", "zu"])
        df_i["type"] = i+1
        df_list.append(df_i)
    df = pd.concat(df_list, ignore_index=True)
    # first type, second xu, third yu, fourth zu
    df = df[["type", "xu", "yu", "zu"]]
    return df