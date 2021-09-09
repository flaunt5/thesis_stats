from tools import data
from stats import cronbach_alpha as ca

first_data = saf.get_first_data("results.csv")

panas_first_num = saf.get_panas_first_num_data(first_data)
gew_first_num = saf.get_gew_first_num_data(first_data)

print(ca.cronbach_alpha(panas_first_num))
print(ca.cronbach_alpha(gew_first_num))
