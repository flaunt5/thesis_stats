import pandas

data = pandas.read_csv("example.csv").drop(index=[0,1]).reset_index()
general_data = data[["Duration (in seconds)", "MT", "AR", "GI", "DEVICE_Browser", "DEVICE_Operating System", "DEVICE_Resolution"]]

# print(general_data.value_counts("MT"))
# print(general_data.value_counts("AR"))
# print(general_data.value_counts("GI"))

ageTime = data[["AR", "Duration (in seconds)"]]
ageTime = ageTime.astype({"AR": "string", "Duration (in seconds)": "int32"})
print(ageTime.dtypes)
# print(ageTime["Duration (in seconds)"])
print(ageTime.groupby("AR").mean())
print(ageTime.groupby("AR").median())

engTime = data[["MT", "Duration (in seconds)"]]
engTime = engTime.astype({"MT": "string", "Duration (in seconds)": "int32"})
print(engTime.dtypes)
# print(ageTime["Duration (in seconds)"])
print(engTime.groupby("MT").mean())
print(engTime.groupby("MT").median())

genTime = data[["GI", "Duration (in seconds)"]]
genTime = genTime.astype({"GI": "string", "Duration (in seconds)": "int32"})
print(genTime.dtypes)
# print(ageTime["Duration (in seconds)"])
print(genTime.groupby("GI").mean())
print(genTime.groupby("GI").median())
