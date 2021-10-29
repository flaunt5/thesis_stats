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

# Fetches the data from the first and second surveys as a data object
FirstData = data.FirstData("first_results/results.csv")
SecondData = data.SecondData(
    "second_results/GEW_resu2.csv", "second_results/PANAS_resu2.csv")

# these variables will store the results using the Geneva Emotion wheel
firstNumGEW = FirstData.get_gew_num_data()
secondNumGEW = SecondData.get_gew_num_data()

# Only preserves results from respondents who answered both surveys
firstNumGEW = firstNumGEW[firstNumGEW.index.isin(
    secondNumGEW.index.values)]
secondNumGEW = secondNumGEW[secondNumGEW.index.isin(
    firstNumGEW.index.values)]

# calculates the Pearsson correlation coefficient between the first and second set of answer per emotion per question
GEWcorr = firstNumGEW.corrwith(secondNumGEW).replace(np.nan, 0)
# applies a fisher Z transformation to all correlation coefficients
GEWcorr = GEWcorr.apply(fisher_z)

# same as above but for results using the PANAS
firstNumPANAS = FirstData.get_panas_num_data()
secondNumPANAS = SecondData.get_panas_num_data()

firstNumPANAS = firstNumPANAS[firstNumPANAS.index.isin(
    secondNumPANAS.index.values)]
secondNumPANAS = secondNumPANAS[secondNumPANAS.index.isin(
    firstNumPANAS.index.values)]


PANAScorr = secondNumPANAS.corrwith(firstNumPANAS).replace(np.nan, 0)
PANAScorr = PANAScorr.apply(fisher_z)

# calculatates the average of the fisher z transformed coefficients and reverse fisher z transforms it
PANASavg = np.tanh(PANAScorr.mean())
GEWavg = np.tanh(GEWcorr.mean())

print(PANASavg)
print(GEWavg)

# standard independent t test on the averages of the pearsson coefficients
ttestavg = sc.ttest_ind(PANASavg, GEWavg)
# standard independent t test on all pearsson correlation coefficients
ttest = sc.ttest_ind(PANAScorr, GEWcorr)

print(ca.cronbach_alpha(firstNumGEW))
print(ca.cronbach_alpha(secondNumGEW))
print(ca.cronbach_alpha(firstNumPANAS))
print(ca.cronbach_alpha(secondNumPANAS))

# previously used to visualize answers in an excel sheet
# GEWsub = secondNumGEW.sub(firstNumGEW)
# PANASsub = secondNumPANAS.sub(firstNumPANAS)

# GEWsub.to_excel("gwsub.xlsx")
# PANASsub.to_excel("panassub.xlsx")
