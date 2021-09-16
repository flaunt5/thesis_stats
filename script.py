from tools import data
from stats import cronbach_alpha as ca
import scipy.stats as sc

# first_data = saf.get_first_data("results.csv")

FirstData = data.FirstData("first_results/results.csv")
SecondData = data.SecondData(
    "second_results/GEW_resu2.csv", "second_results/PANAS_resu2.csv")

firstAssocGEW = FirstData.get_gew_assoc_data()
secondAssocGEW = SecondData.get_gew_assoc_data()

print(FirstData.get_gew_num_data())
exit()
for index, row in firstAssocGEW:
    print(index)
    print(row)
    exit()

# panas_first_num = saf.get_panas_first_num_data(first_data)
# gew_first_num = saf.get_gew_first_num_data(first_data)

# print(ca.cronbach_alpha(panas_first_num))
# print(ca.cronbach_alpha(gew_first_num))

# print(gew_first_num)

print(sc.pearsonr(firstNumGEW, secondNumGEW))
