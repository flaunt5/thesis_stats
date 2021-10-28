from tools import data
from stats import cronbach_alpha as ca
import scipy.stats as sc
import pandas as pd
import numpy as np

# first_data = saf.get_first_data("results.csv")

# returns a Fisher-Z transform, which is equivalent to the Inverse hyperbolic tangent according to https://stats.stackexchange.com/questions/109028/fishers-z-transform-in-python
def fisher_z(input):
    if (input > 1.0):
        num = input + 0j
        return np.arctanh(num)
    return input

FirstData = data.FirstData("first_results/results.csv")
SecondData = data.SecondData(
    "second_results/GEW_resu2.csv", "second_results/PANAS_resu2.csv")

firstNumGEW = FirstData.get_gew_num_data()
secondNumGEW = SecondData.get_gew_num_data()

firstNumGEW = firstNumGEW[firstNumGEW.index.isin(
    secondNumGEW.index.values)]
secondNumGEW = secondNumGEW[secondNumGEW.index.isin(
    firstNumGEW.index.values)]

GEWcorr = firstNumGEW.corrwith(secondNumGEW).replace(np.nan, 0)
GEWcorr = GEWcorr.apply(fisher_z)
firstNumPANAS = FirstData.get_panas_num_data()
secondNumPANAS = SecondData.get_panas_num_data()

firstNumPANAS = firstNumPANAS[firstNumPANAS.index.isin(
    secondNumPANAS.index.values)]
secondNumPANAS = secondNumPANAS[secondNumPANAS.index.isin(
    firstNumPANAS.index.values)]


PANAScorr = secondNumPANAS.corrwith(firstNumPANAS).replace(np.nan, 0)
PANAScorr = PANAScorr.apply(fisher_z)

PANASavg = np.tanh(PANAScorr.mean())
GEWavg = np.tanh(GEWcorr.mean())

print(PANASavg)
print(GEWavg)

ttestavg = sc.ttest_ind(PANASavg, GEWavg)
ttest = sc.ttest_ind(PANAScorr, GEWcorr)

print(ca.cronbach_alpha(firstNumGEW))
print(ca.cronbach_alpha(secondNumGEW))
print(ca.cronbach_alpha(firstNumPANAS))
print(ca.cronbach_alpha(secondNumPANAS))

# GEWsub = secondNumGEW.sub(firstNumGEW)
# PANASsub = secondNumPANAS.sub(firstNumPANAS)

# GEWsub.to_excel("gwsub.xlsx")
# PANASsub.to_excel("panassub.xlsx")
