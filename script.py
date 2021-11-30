from tools import data
from tools import demographic_data
from stats import cronbach_alpha as ca
from stats import correlation as cr
from stats import welch as w
import scipy.stats as sc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff

pd.options.plotting.backend = "plotly"

transpose = 0

dem = demographic_data.get_demographic_data(
    "first_results/results.csv", "second_results/GEW_resu2.csv", "second_results/PANAS_resu2.csv")
dem = dem[dem["Duration (first)"] < 10000]
demGEW = dem[dem["Method"] == "GEW"]
demPANAS = dem[dem["Method"] == "PANAS"]


def dem_dataframe(column, name):
    return pd.concat(
        [demGEW[column].value_counts().append(
            pd.Series(demGEW[column].value_counts().sum(), index=["Total"])),
         demPANAS[column].value_counts().append(
            pd.Series(demPANAS[column].value_counts().sum(), index=["Total"])),
         dem[column].value_counts().append(
            pd.Series(dem[column].value_counts().sum(), index=["Total"]))],
        axis=1).fillna(0).sort_index().reset_index().rename(columns={"index": name, 0: "GEW", 1: "PANAS", 2: "Combined"}).set_index(name)


df_ar = dem_dataframe("AR", "Age Range")
df_mt = dem_dataframe("MT", "English as Mother Tongue").reindex(
    ["Yes", "No", "Prefer not to say"])
df_gi = dem_dataframe("GI", "Gender Identity")
df_duration = pd.DataFrame([("First", demGEW["Duration (first)"].mean(),
                            demPANAS["Duration (first)"].mean(),
                            dem["Duration (first)"].mean()),
                           ("Second", demGEW["Duration (second)"].mean(),
                            demPANAS["Duration (second)"].mean(),
                           dem["Duration (second)"].mean())],
                           columns=["Survey Round", "GEW", "PANAS", "Combined"]).set_index("Survey Round")

print("\n# Shapiro Wilk test on time taken on the first surveys\n    ",
      sc.shapiro(dem["Duration (first)"]))
print("\n# Shapiro Wilk test on time taken on the second surveys\n    ",
      sc.shapiro(dem["Duration (second)"]))

demM = dem["Method"].apply(
    lambda x: True if x == "GEW" else False)
mw1 = sc.mannwhitneyu(
    demGEW["Duration (first)"], demPANAS["Duration (first)"], alternative="greater")
pbs1 = sc.pointbiserialr(demM, dem["Duration (first)"])
mw2 = sc.mannwhitneyu(
    demGEW["Duration (second)"], demPANAS["Duration (second)"], alternative="greater")
pbs2 = sc.pointbiserialr(demM, dem["Duration (second)"])

df_mannwhit_pbs = pd.DataFrame([("First", mw1.statistic, mw1.pvalue, pbs1.correlation, pbs1.pvalue), ("Second", mw2.statistic, mw2.pvalue, pbs2.correlation, pbs2.pvalue)],
                               columns=["Survey Round", "MW Statistic", "MW P-value", "PB Correlation", "PB P-value"]).set_index("Survey Round")


print("\n# Mann Whitney test comparing time taken for the the first and second rounds of surveys:\n    ",
      sc.mannwhitneyu(dem["Duration (first)"], dem["Duration (second)"]))

ar_k1 = sc.kruskal(*[group["Duration (first)"].values for name,
                   group in dem[["AR", "Duration (first)"]].groupby("AR")])
mt_k1 = sc.kruskal(*[group["Duration (first)"].values for name,
                   group in dem[["MT", "Duration (first)"]].groupby("MT")])
gi_k1 = sc.kruskal(*[group["Duration (first)"].values for name,
                   group in dem[["GI", "Duration (first)"]].groupby("GI")])

ar_k2 = sc.kruskal(*[group["Duration (second)"].values for name,
                   group in dem[["AR", "Duration (second)"]].groupby("AR")])
mt_k2 = sc.kruskal(*[group["Duration (second)"].values for name,
                   group in dem[["MT", "Duration (second)"]].groupby("MT")])
gi_k2 = sc.kruskal(*[group["Duration (second)"].values for name,
                   group in dem[["GI", "Duration (second)"]].groupby("GI")])

df_kruskal = pd.DataFrame([("First", ar_k1.pvalue, mt_k1.pvalue, gi_k1.pvalue), ("Second", ar_k2.pvalue, mt_k2.pvalue, gi_k2.pvalue)],
                          columns=["Survey Round", "Age Range", "English as Mother Tongue", "Gender Identity"]).set_index("Survey Round")

# Fetches the data from the first and second surveys as a data object
FirstData = data.FirstData("first_results/results.csv")
SecondData = data.SecondData(
    "second_results/GEW_resu2.csv", "second_results/PANAS_resu2.csv")

numData = data.get_num_data_per_method(FirstData, SecondData)
numDataGEW = numData['GEW']
numDataPANAS = numData['PANAS']

df_cronbach = pd.DataFrame([("First", str(ca.cronbach_alpha(
    numDataGEW[0])), str(ca.cronbach_alpha(numDataPANAS[0]))), ("Second", ca.cronbach_alpha(numDataGEW[1]), ca.cronbach_alpha(numDataPANAS[1]))],
    columns=["Survey Round", "GEW", "PANAS"]).set_index("Survey Round")

corrGEW = cr.get_correlation(numDataGEW[0], numDataGEW[1], transpose)
corrPANAS = cr.get_correlation(numDataPANAS[0], numDataPANAS[1], transpose)
lossGEW = cr.loss_calc(corrGEW[1], corrGEW[0])
lossPANAS = cr.loss_calc(corrPANAS[1], corrPANAS[0])

print("\n# Correlations calculated with the following data losses:")
print("     GEW: loss of " +
      str(lossGEW[0]) + " datapoints out of " + str(lossGEW[1]) + ", corresponding to " + str(lossGEW[2]) + " %")
print("     PANAS: loss of " +
      str(lossPANAS[0]) + " datapoints out of " + str(lossPANAS[1]) + ", corresponding to " + str(lossPANAS[2]) + "%")
corrGEW = corrGEW[0]
corrPANAS = corrPANAS[0]

print("# Shapiro Wilk test of normality for the Fisher-Z transformed GEW correlations:\n  ", sc.shapiro(corrGEW))
print("# Shapiro Wilk test of normality for the Fisher-Z transformed PANAS correlations:\n  ",
      sc.shapiro(corrPANAS))
print("# Mann Whitney U test of similarity of the media of the Fisher-Z transformed GEW and PANAS correlations:\n   ",
      sc.mannwhitneyu(corrGEW, corrPANAS))


corrGEW_n = len(corrGEW)
corrPANAS_n = len(corrPANAS)

df_ttest = w.welch_ttest(corrGEW, corrPANAS)
avgGEW = cr.get_weighted_average_corr(corrGEW)
avgPANAS = cr.get_weighted_average_corr(corrPANAS)
stdGEW = float(np.nanstd(corrGEW, ddof=1))
stdPANAS = float(np.nanstd(corrPANAS, ddof=1))
semGEW = float(sc.sem(corrGEW, nan_policy='omit'))
semPANAS = float(sc.sem(corrPANAS, nan_policy='omit'))

df_corr = pd.DataFrame([("Weighted Average of Correlations (Fisher-Z transformed)", avgGEW, avgPANAS),
                        ("Standard Deviation", stdGEW, stdPANAS),
                        ("Standard Error", semGEW, semPANAS),
                        ("Weighted Average (back-transformed)", np.tanh(avgGEW), np.tanh(avgPANAS))],
                       columns=["Measure", "GEW", "PANAS"]).set_index("Measure")
cocorr = cr.independent_correlation_test(
    avgGEW, avgPANAS, corrGEW_n, corrPANAS_n)

print("\n# Significance test on the average correlations for GEW and PANAS:")
print("     t-statistic: ", str(cocorr),
      "\n   p-value: ", str(sc.norm.sf(abs(cocorr))*2))


with pd.ExcelWriter("graphs/demographics.xlsx") as writerD:
    df_ar.to_excel(writerD, sheet_name="Age Range")
    df_mt.to_excel(writerD, sheet_name="Mother Tongue")
    df_gi.to_excel(writerD, sheet_name="Gender Identity")


with pd.ExcelWriter("graphs/stats.xlsx") as writerS:
    df_duration.to_excel(writerS, sheet_name="Duration")
    df_cronbach.to_excel(writerS, sheet_name="Cronbach")
    df_mannwhit_pbs.to_excel(writerS, sheet_name="MannWhit PBS")
    df_kruskal.to_excel(writerS, sheet_name="Kruskal")
    df_ttest.to_excel(writerS, sheet_name="T-test")
    df_corr.to_excel(writerS, sheet_name="Corr")

fig = ff.create_distplot([corrGEW.values, corrPANAS.values], [
                         'GEW', "PANAS"], bin_size=.2)
fig.write_image("graphs/corr_distplot.jpg")

test = go.Figure(data=[
      go.Bar(name="First", x=df_duration.columns.values, y=df_duration.loc["First", :].values,
             error_y=dict(type='data', array=[sc.sem(demGEW['Duration (first)']), sc.sem(demPANAS['Duration (first)']), sc.sem(dem['Duration (first)'])])),
      go.Bar(name="Second", x=df_duration.columns.values, y=df_duration.loc["Second", :].values,
             error_y=dict(type='data', array=[sc.sem(demGEW['Duration (second)']), sc.sem(demPANAS['Duration (second)']), sc.sem(dem['Duration (second)'])]))
])
test.update_layout(barmode='group')
test.write_image("graphs/duration_mean_bars.jpg")
