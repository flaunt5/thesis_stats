from tools import data
from stats import cronbach_alpha as ca
from stats import correlation as cr
from stats import general as gn
from stats import welch as w
import scipy.stats as sc
import pandas as pd
import numpy as np
import krippendorff as k
import plotly.graph_objects as go

transpose = 0

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

corrGEW = cr.get_correlation(numDataGEW[0], numDataGEW[1], transpose)
corrPANAS = cr.get_correlation(numDataPANAS[0], numDataPANAS[1], transpose)
lossGEW = cr.loss_calc(corrGEW[1], corrGEW[0])
lossPANAS = cr.loss_calc(corrPANAS[1], corrPANAS[0])

print("\n#Correlations calculated with the following data losses:")
print(" GEW: loss of " +
      str(lossGEW[0]) + " datapoints out of " + str(lossGEW[1]) + ", corresponding to " + str(lossGEW[2]) + " %")
print(" PANAS: loss of " +
      str(lossPANAS[0]) + " datapoints out of " + str(lossPANAS[1]) + ", corresponding to " + str(lossPANAS[2]) + "%")
corrGEW = corrGEW[0]
corrPANAS = corrPANAS[0]
corrGEW_n = len(corrGEW)
corrPANAS_n = len(corrPANAS)


print("\n#Independent T test of GEW correlations against PANAS:\n   " +
      str(w.welch_ttest(corrGEW, corrPANAS)))

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

avgGEW = cr.get_weighted_average_corr(corrGEW)
avgPANAS = cr.get_weighted_average_corr(corrPANAS)

intervalGEW = sc.t.interval(
    alpha=0.95, df=corrGEW_n-1, loc=avgGEW, scale=semGEW)
intervalPANAS = sc.t.interval(
    alpha=0.95, df=corrPANAS_n-1, loc=avgPANAS, scale=semPANAS)

print("\n#Average Fisher-Z transformed correlation for:")
print(" GEW results: " + str(avgGEW) +
      ", confidence interval: " + str(intervalGEW))
print(" PANAS results: " + str(avgPANAS) +
      ", confidence interval: " + str(intervalPANAS))

print("\n#Fisher-Z back-transformed Average correlation for:")
print(" GEW results: " + str(np.tanh(avgGEW)))
print(" PANAS results: " + str(np.tanh(avgPANAS)))

cocorr = cr.independent_correlation_test(
    avgGEW, avgPANAS, corrGEW_n, corrPANAS_n)

print("\nSignificance test on the average correlations for GEW and PANAS:")
print(" t-statistic: " + str(cocorr) +
      " p-value: " + str(sc.norm.sf(abs(cocorr))*2))


# previously used to visualize answers in an excel sheet
# GEWsub = secondNumGEW.sub(firstNumGEW)
# PANASsub = secondNumPANAS.sub(firstNumPANAS)

# GEWsub.to_excel("gwsub.xlsx")
# PANASsub.to_excel("panassub.xlsx")


fig = go.Figure(data=[
      go.Bar(name='method',
      x=["GEW", "PANAS"],
      y=[avgGEW, avgPANAS],
      error_y=dict(type='data', array=[semGEW, semPANAS])
      )
])
fig.update_yaxes(range=[0, 1])
# fig.update_layout(barmode='group')
fig.show()
