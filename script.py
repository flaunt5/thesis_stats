from tools import data
import stats as st
import scipy.stats as sc
import pandas as pd
import numpy as np

# first_data = saf.get_first_data("results.csv")

# returns a Fisher-Z transform, which is equivalent to the Inverse hyperbolic tangent according to https://stats.stackexchange.com/questions/109028/fishers-z-transform-in-python
def fisher_z(input):
    print(input)
    exit()
    num = input + 0j
    print(num)
    return np.arctanh(num, 1)

FirstData = data.FirstData("first_results/results.csv")
SecondData = data.SecondData(
    "second_results/GEW_resu2.csv", "second_results/PANAS_resu2.csv")

# firstAssocGEW = FirstData.get_gew_assoc_data()[['EMAIL']]
# secondAssocGEW = SecondData.get_gew_assoc_data()[['RecipientEmail1']]

# print(firstAssocGEW)
# print(secondAssocGEW)

firstNumGEW = FirstData.get_gew_num_data()
secondNumGEW = SecondData.get_gew_num_data()

firstNumGEW = firstNumGEW[firstNumGEW.index.isin(
    secondNumGEW.index.values)]
secondNumGEW = secondNumGEW[secondNumGEW.index.isin(
    firstNumGEW.index.values)]

GEWcorr = firstNumGEW.corrwith(secondNumGEW)
GEWcorr = GEWcorr.apply(fisher_z)

firstNumPANAS = FirstData.get_panas_num_data()
secondNumPANAS = SecondData.get_panas_num_data()

firstNumPANAS = firstNumPANAS[firstNumPANAS.index.isin(
    secondNumPANAS.index.values)]
secondNumPANAS = secondNumPANAS[secondNumPANAS.index.isin(
    firstNumPANAS.index.values)]


PANAScorr = firstNumPANAS.corrwith(secondNumPANAS).replace(np.inf, 0).replace(np.nan, 0)
print(PANAScorr.values)
PANAScorr = PANAScorr.apply(fisher_z)
exit()
PANASavg = PANAScorr.dropna().values
GEWavg = GEWcorr.dropna().values

print(PANASavg)
print(GEWavg)
exit;

ttesst = sc.ttest_ind(PANAScorr, GEWcorr)



# print(GEWcorr)
# print(PANAScorr)

# firstGEWvalues = firstNumGEW.to_numpy().flatten()
# secondGEWvalues = secondNumGEW.to_numpy().flatten()
# firstPANASvalues = firstNumPANAS.to_numpy().flatten()
# secondPANASvalues = secondNumPANAS.to_numpy().flatten()
# print(sc.pearsonr(firstGEWvalues, secondGEWvalues))
# print(sc.pearsonr(firstPANASvalues, secondPANASvalues))

# GEWsub = secondNumGEW.sub(firstNumGEW)
# PANASsub = secondNumPANAS.sub(firstNumPANAS)

# GEWsub.to_excel("gwsub.xlsx")
# PANASsub.to_excel("panassub.xlsx")
