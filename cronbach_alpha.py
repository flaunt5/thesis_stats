import pandas as pd
import numpy as np

def cronbach_alpha(df):
    df_corr = df.corr()
    N = df.shape[1]
    rs = np.array([])
    df_corr = df_corr.fillna(0)

    for i, col in enumerate(df_corr.columns):
        sum_ = df_corr[col][i+1:].values
        rs = np.append(sum_, rs)
    mean_r = np.mean(rs)
    return (N * mean_r) / (1 + (N - 1) * mean_r)
