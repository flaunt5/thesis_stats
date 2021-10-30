from tools import data
from stats import cronbach_alpha as ca
from stats import correlation as cr
from stats import general as gn
import scipy.stats as sc
import pandas as pd
import numpy as np
import krippendorff as k

# Fetches the data from the first and second surveys as a data object
FirstData = data.FirstData("first_results/results.csv")
SecondData = data.SecondData(
    "second_results/GEW_resu2.csv", "second_results/PANAS_resu2.csv")

numData = data.get_num_data_per_method(FirstData, SecondData)
numDataGEW = numData['GEW']
numDataPANAS = numData['PANAS']

print("#N population size for: ")
print(" GEW survey: " + str(len(numData['GEW'][0])))
print(" PANAS survey: " + str(len(numData['PANAS'][0])))

print("\n#Cronbach's Alpha for...")
print(" First GEW survey results: " + str(ca.cronbach_alpha(numDataGEW[0])))
print(" Second GEW survey results: " + str(ca.cronbach_alpha(numDataGEW[1])))
print(" First PANAS survey results: " +
      str(ca.cronbach_alpha(numDataPANAS[0])))
print(" Second GEW survey results: " + str(ca.cronbach_alpha(numDataPANAS[1])))

print("\n#Krippendorff's Alpha for...")
print(" First GEW survey results: " + str(k.alpha(numDataGEW[0])))
print(" Second GEW survey results: " + str(k.alpha(numDataGEW[1])))
print(" First PANAS survey results: " + str(k.alpha(numDataPANAS[0])))
print(" Second GEW survey results: " + str(k.alpha(numDataPANAS[1])))

corrGEW = cr.get_correlation(numDataGEW[0], numDataGEW[1])
corrPANAS = cr.get_correlation(numDataPANAS[0], numDataPANAS[1])
corrGEW_n = len(corrGEW)
corrPANAS_n = len(corrPANAS)

print("\n#Independent T test of GEW correlations against PANAS:\n   " +
      str(sc.ttest_ind(corrGEW.apply(cr.inf_to_real), corrPANAS.apply(cr.inf_to_real), nan_policy='omit', equal_var=sc.tvar(corrGEW) == sc.tvar(corrPANAS))))

stdGEW = float(np.nanstd(corrGEW, ddof=1))
stdPANAS = float(np.nanstd(corrPANAS, ddof=1))
print("\n#Standard deviations for: ")
print(" GEW correlations: " + str(stdGEW))
print(" PANAS correlations: " + str(stdPANAS))

semGEW = float(sc.sem(corrGEW, nan_policy='omit'))
semPANAS = float(sc.sem(corrPANAS, nan_policy='omit'))
print("\n#Standard errors for: ")
print(" GEW correlations: " + str(semGEW))
print(" PANAS correlations: " + str(semPANAS))

intervalGEW = sc.t.interval(
    alpha=0.95, df=corrGEW_n-1, loc=np.mean(corrGEW.apply(cr.inf_to_real)), scale=semGEW)
intervalPANAS = sc.t.interval(
    alpha=0.95, df=corrPANAS_n-1, loc=np.mean(corrPANAS.apply(cr.inf_to_real)), scale=semPANAS)

print(intervalGEW)
print(intervalPANAS)

avgGEW = cr.get_average_corr(corrGEW)
avgPANAS = cr.get_average_corr(corrPANAS)

print("\n#Average correlation for:")
print(" GEW results: " + str(avgGEW.real + avgPANAS.imag))
print(" PANAS results: " + str(avgPANAS.real + avgPANAS.imag))

cocorr = cr.independent_correlation_test(corrGEW.mean(), corrPANAS.mean(), corrGEW_n, corrPANAS_n)

print(cocorr)


# previously used to visualize answers in an excel sheet
# GEWsub = secondNumGEW.sub(firstNumGEW)
# PANASsub = secondNumPANAS.sub(firstNumPANAS)

# GEWsub.to_excel("gwsub.xlsx")
# PANASsub.to_excel("panassub.xlsx")
