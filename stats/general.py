import pandas as pd
import numpy as np
import scipy.stats as sc


def get_data():
    MTcorrespondence = {3: "Yes", 4: "No", 5: "Prefer not to say"}
    ARcorrespondence = {1: "Under 18", 2: "18-24", 3: "25-34", 4: "35-44", 5: "45-54",
                        6: "55-64", 7: "65-74", 8: "75-84", 9: "85 or older", 10: "Prefer not to say"}
    GIcorrespondence = {1: "Male", 2: "Female",
                        3: "Non-binary/third gender", 4: "Prefer not to say"}
    data = pd.read_csv(
        "first_results/results.csv").drop(index=[0, 1]).reset_index()

    data['method'] = np.where(pd.isna(data["Q2.1_1"]), "PANAS", "GEW")

    general_data = data[["Duration (in seconds)", "MT", "AR", "GI", "method"]].astype(
        {"Duration (in seconds)": "int32", "MT": "int32", "AR": "int32", "GI": "int32", "method": "string"})

    general_data = general_data.replace(
        {"MT": MTcorrespondence, "AR": ARcorrespondence, "GI": GIcorrespondence}).astype({"MT": "string", "AR": "string", "GI": "string"})
    return general_data


def duration_mean_spearman(dataset, column):
    data = dataset[[column, "Duration (in seconds)"]]
    mean = data.groupby(column).mean()
    spear = sc.spearmanr(data[column].tolist(),
                         data['Duration (in seconds)'].tolist())
    return [mean, spear]


def get_data_categories(dataset):
    ar = duration_mean_spearman(dataset, "AR")
    mt = duration_mean_spearman(dataset, "MT")
    gi = duration_mean_spearman(dataset, "GI")
    return {"AR": ar, "MT": mt, "GI": gi}


# general_data = get_data()
# per_method = duration_mean_spearman(general_data, "method")
# print(per_method)
# general_cat = get_data_categories(general_data)
# print(general_cat)

# gew_data = general_data[general_data["method"] == "GEW"]
# gew_cat = get_data_categories(gew_data)
# print(gew_cat)

# panas_data = general_data[general_data["method"] == "PANAS"]
# panas_cat = get_data_categories(panas_data)
# print(panas_cat)
