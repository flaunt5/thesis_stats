from tools import data
from stats import cronbach_alpha as ca
import scipy.stats as sc
import pandas as pd

# first_data = saf.get_first_data("results.csv")

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

firstNumPANAS = FirstData.get_panas_num_data()
secondNumPANAS = SecondData.get_panas_num_data()

firstNumPANAS = firstNumPANAS[firstNumPANAS.index.isin(
    secondNumPANAS.index.values)]
secondNumPANAS = secondNumPANAS[secondNumPANAS.index.isin(
    firstNumPANAS.index.values)]

firstGEWvalues = firstNumGEW.to_numpy().flatten()
secondGEWvalues = secondNumGEW.to_numpy().flatten()
firstPANASvalues = firstNumPANAS.to_numpy().flatten()
secondPANASvalues = secondNumPANAS.to_numpy().flatten()
print(sc.pearsonr(firstGEWvalues, secondGEWvalues))
print(sc.pearsonr(firstPANASvalues, secondPANASvalues))

# GEWsub = secondNumGEW.sub(firstNumGEW)
# PANASsub = secondNumPANAS.sub(firstNumPANAS)

# GEWsub.to_excel("gwsub.xlsx")
# PANASsub.to_excel("panassub.xlsx")
