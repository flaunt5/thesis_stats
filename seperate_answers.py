import pandas
import numpy
import cronbach_alpha as ca

data = pandas.read_csv("results.csv").drop(index=[0, 1]).reset_index()

gew_data = data[pandas.isna(data["Q2.1_1"])]
panas_data = data[pandas.notna(data["Q2.1_1"])]

gew_data_num = gew_data.iloc[:, 383:777]
gew_data_num = gew_data_num
gew_data_other = gew_data[['ResponseId', 'Duration (in seconds)', 'EMAIL']]
gew_data = gew_data_other.join(gew_data_num)

panas_data_num = panas_data.iloc[:, 22:382]
panas_data_num = panas_data_num.fillna(1)
panas_data_num = panas_data_num.apply(pandas.to_numeric)
panas_data_other = panas_data[['ResponseId', 'Duration (in seconds)', 'EMAIL']]
panas_data = panas_data_other.join(panas_data_num)

# numpy.savetxt("first_results/results_gew.csv", gew_data, delimiter=", ", fmt="% s")
# numpy.savetxt("first_results/results_panas.csv", panas_data, delimiter=", ", fmt="% s")


print(ca.cronbach_alpha(panas_data_num))
print(ca.cronbach_alpha(panas_data_num))
