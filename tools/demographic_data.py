import pandas as pd
import numpy as np


def get_demographic_data(firstFile, secondFileGEW, secondFilePANAS):
    MTcorrespondence = {3: "Yes", 4: "No", 5: "Prefer not to say"}
    ARcorrespondence = {1: "Under 18", 2: "18-24", 3: "25-34", 4: "35-44", 5: "45-54",
                        6: "55-64", 7: "65-74", 8: "75-84", 9: "85 or older", 10: "Prefer not to say"}
    GIcorrespondence = {1: "Male", 2: "Female",
                        3: "Non-binary/third gender", 4: "Prefer not to say"}
    data = pd.read_csv(firstFile).drop(index=[0, 1]).reset_index()
    data.rename({"ResponseId": "ID", "Duration (in seconds)": "Duration (first)"}, axis="columns", inplace=True)
    data.set_index("ID", inplace=True)
    data.sort_index(inplace=True)

    GEWtwo = pd.read_csv(secondFileGEW).drop(index=[0, 1]).reset_index()
    PANAStwo = pd.read_csv(secondFilePANAS).drop(index=[0, 1]).reset_index()
    dataTwo = pd.concat([GEWtwo, PANAStwo])[["ID", "Duration (in seconds)"]].astype({"Duration (in seconds)": "int32"})
    dataTwo.rename(
        {"Duration (in seconds)": "Duration (second)"}, axis="columns", inplace=True)
    dataTwo.set_index("ID", inplace=True)
    dataTwo.sort_index(inplace=True)

    data = data[data.index.isin(dataTwo.index.values)]
    data['Method'] = np.where(pd.isna(data["Q2.1_1"]), "PANAS", "GEW")

    data = data[["Duration (first)", "MT", "AR", "GI", "Method"]].astype(
        {"Duration (first)": "int32", "MT": "int32", "AR": "int32", "GI": "int32", "Method": "string"})
    

    data = data.replace(
        {"MT": MTcorrespondence, "AR": ARcorrespondence, "GI": GIcorrespondence}).astype({"MT": "string", "AR": "string", "GI": "string"})
    
    return data.join(dataTwo)[["Method", "AR", "GI", "MT", "Duration (first)", "Duration (second)"]]




