import pandas
import numpy


def get_first_data(file):
    return pandas.read_csv(file).drop(index=[0, 1]).reset_index()


def get_gew_first_data(data):
    otherCols = ['OTHER1', 'OTHER2', 'OTHER3', 'OTHER4', 'OTHER5', 'OTHER6', 'OTHER7', 'OTHER8', 'OTHER9',
                 'OTHER10', 'OTHER11', 'OTHER12', 'OTHER13', 'OTHER14', 'OTHER15', 'OTHER16', 'OTHER17', 'OTHER18']

    gew_data = data[pandas.isna(data["Q2.1_1"])]

    gew_data_num = gew_data.iloc[:, 383:778]
    gew_data_num = gew_data_num.drop(otherCols, axis=1).fillna(0).astype(int)

    gew_data_index = gew_data[['ResponseId', 'Duration (in seconds)', 'EMAIL']].astype(
        {'ResponseId': 'string', 'Duration (in seconds)': 'int64', 'EMAIL': 'string'})

    gew_data_other = gew_data[otherCols].fillna("").astype(str)

    return [gew_data_num, gew_data_index, gew_data_other]


def get_gew_first_num_data(data):
    return get_gew_first_data(data)[0]


def get_gew_first_assoc_data(data):
    gew_data = get_gew_first_data(data)
    return gew_data[1].join(gew_data[0])


def get_gew_first_other_data(data):
    gew_data = get_gew_first_data(data)
    return gew_data[1].join(gew_data[2])


def get_panas_first_data(data):
    panas_data = data[pandas.notna(data["Q2.1_1"])]

    panas_data_num = panas_data.iloc[:, 22:382].fillna(
        1).apply(pandas.to_numeric)

    panas_data_index = panas_data[['ResponseId', 'Duration (in seconds)', 'EMAIL']].astype(
        {'ResponseId': 'string', 'Duration (in seconds)': 'int64', 'EMAIL': 'string'})

    return [panas_data_num, panas_data_index]


def get_panas_first_num_data(data):
    return get_panas_first_data(data)[0]


def get_panas_first_assoc_data(data):
    panas_data = get_panas_first_data(data)
    return panas_data[1].join(panas_data[0])


def write_to_csv(data, filepath):
    numpy.savetxt(filepath,
                  data, delimiter=", ", fmt="% s")

def seperate_answers_first(file):
    data = get_first_data(file)
    write_to_csv(get_gew_first_assoc_data(data),
                 "first_results/results_gew.csv")
    write_to_csv(get_gew_first_other_data(data),
                 "first_results/results_gew_other.csv")
    write_to_csv(get_panas_first_assoc_data(data),
                 "first_results/results_panas.csv")

