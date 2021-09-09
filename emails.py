import pandas
import numpy

data = pandas.read_csv("results.csv").drop(index=[0, 1]).reset_index()
email_data = data[["ResponseId", "EMAIL", "Q2.1_1"]]
email_data = email_data.astype(
    {"ResponseId": "string", "EMAIL": "string", "Q2.1_1": "string"})
email_data = email_data[email_data.EMAIL.notnull()]

emails_panas = [["Email", "ID"]]
emails_gew = [["Email", "ID"]]

for index, row in email_data.iterrows():
    check = pandas.isna(row["Q2.1_1"])
    if(check):
        emails_panas.append([row["EMAIL"], row["ResponseId"]])
    else:
        emails_gew.append([row["EMAIL"], row["ResponseId"]])

numpy.savetxt("emails_gew.csv", emails_gew, delimiter = ", ", fmt = "% s")
numpy.savetxt("emails_panas.csv", emails_panas, delimiter=", ", fmt="% s")
