import numpy
from data import FirstData, SecondData


def write_to_csv(data, filepath):
    numpy.savetxt(filepath,
                  data, delimiter=", ", fmt="% s")


def seperate_answers_first(file):
    data = FirstData(file)
    write_to_csv(data.get_gew_assoc_data(),
                 "first_results/results_gew.csv")
    write_to_csv(data.get_gew_other_data(),
                 "first_results/results_gew_other.csv")
    write_to_csv(data.get_panas_assoc_data(),
                 "first_results/results_panas.csv")


def seperate_answers_second(file_gew, file_panas):
    data = SecondData(file_gew, file_panas)
    write_to_csv(data.get_gew_assoc_data(),
                 "second_results/results_gew.csv")
    write_to_csv(data.get_gew_other_data(),
                 "second_results/results_gew_other.csv")
    write_to_csv(data.get_panas_assoc_data(),
                 "second_results/results_panas.csv")


seperate_answers_first("first_results/results.csv")
seperate_answers_second("second_results/GEW_resu2.csv",
                        "second_results/PANAS_resu2.csv")
