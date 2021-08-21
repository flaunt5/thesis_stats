import pandas
import numpy

data = pandas.read_csv("example2.csv").drop(index=[0, 1]).reset_index()
email_data = data[["EMAIL", "Q2.1_1"]]
email_data= email_data.astype({"EMAIL": "string", "Q2.1_1" : "string"})
email_data = email_data[email_data.EMAIL.notnull()]

emails_panas = [["Email"]]
emails_gew = [["Email"]]

for index, row in email_data.iterrows():
    check = pandas.isna(row["Q2.1_1"])
    if(check):
        emails_panas.append([row["EMAIL"]])
    else:
        emails_gew.append([row["EMAIL"]])

numpy.savetxt("emails_gew.csv", emails_gew, delimiter = ", ", fmt = "% s")
numpy.savetxt("emails_panas.csv", emails_panas, delimiter=", ", fmt="% s")
