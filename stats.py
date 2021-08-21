import pandas

data = pandas.read_csv("example2.csv").drop(index=[0,1]).reset_index()
general_data = data[["Duration (in seconds)", "MT", "AR", "GI", "DEVICE_Browser", "DEVICE_Operating System", "DEVICE_Resolution", "EMAIL"]]
general_data = general_data[general_data.EMAIL.notnull()]

# print(general_data.value_counts("MT"))
print(general_data.value_counts("AR"))
print(general_data.value_counts("GI"))


ageTime = data[["AR", "Duration (in seconds)"]]
ageTime = ageTime.astype({"AR": "string", "Duration (in seconds)": "int32"})
print(ageTime.groupby("AR").mean())
print(ageTime.groupby("AR").median())

engTime = data[["MT", "Duration (in seconds)"]]
engTime = engTime.astype({"MT": "string", "Duration (in seconds)": "int32"})
print(engTime.groupby("MT").mean())
print(engTime.groupby("MT").median())

genTime = data[["GI", "Duration (in seconds)"]]
genTime = genTime.astype({"GI": "string", "Duration (in seconds)": "int32"})
print(genTime.groupby("GI").mean())
print(genTime.groupby("GI").median())
