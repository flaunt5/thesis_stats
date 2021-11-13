import pandas as pd
import numpy as np
import scipy.stats as sc
import plotly.graph_objects as go


pd.options.plotting.backend = "plotly"

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

def ttest_duration_per_method(dataset):
    gew_data = dataset[dataset["method"] == "GEW"]
    gew_data = gew_data["Duration (in seconds)"].tolist()
    panas_data = dataset[dataset["method"] == "PANAS"]
    panas_data = panas_data["Duration (in seconds)"].tolist()
    return sc.ttest_ind(gew_data, panas_data, equal_var=False)


def duration_mean_spearman(dataset, column):
    data = dataset[[column, "Duration (in seconds)"]]
    mean = data.groupby(column).mean()
    spear = sc.spearmanr(data[column].tolist(),
                         data['Duration (in seconds)'].tolist())
    return [mean, spear]

def point_biserial(dataset, column="method"):
    data = dataset[[column, "Duration (in seconds)"]]
    data[column] = data[column].apply(lambda x: True if (x == "GEW" or x == "Yes") else False)
    return sc.pointbiserialr(data[column], data["Duration (in seconds)"])


general_data = get_data()
gew_data = general_data[general_data["method"] == "GEW"]
panas_data = general_data[general_data["method"] == "PANAS"]

shapiro = sc.shapiro(general_data['Duration (in seconds)'].tolist())

test = sc.kruskal(*[group["Duration (in seconds)"].values for name,
                  group in general_data[["method", "Duration (in seconds)"]].groupby("method")])


print(test)

print(ttest_duration_per_method(general_data))

print(point_biserial(general_data))
print(point_biserial(general_data, "MT"))



