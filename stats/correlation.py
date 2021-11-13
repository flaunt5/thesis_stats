import numpy as np
import pandas as pd
import scipy.stats as sc


# returns a Fisher-Z transform, which is equivalent to the Inverse hyperbolic tangent according to https://stats.stackexchange.com/questions/109028/fishers-z-transform-in-python
# input is first transformed into a complex number to prevent returning `inf`
def fisher_z(input: float) -> complex:
    if (input > 1.0):
        num = input + 0j
        return np.arctanh(num)
    return input


# calculates the Pearsson correlation coefficient between the first and second set of answers
# by default will calculate them per emotion per question, set axis=1 to calculate per respondent
# then applies a fisher Z transformation to all correlation coefficients
def get_correlation(first_data: pd.DataFrame, second_data: pd.DataFrame, axis=0, replace=True) -> pd.DataFrame:
    # corr = first_data.corrwith(second_data, axis)
    results = list()
    ind = list()
    data_loss = 0
    if (axis == 0):
        first_data = first_data.transpose()
    else:
        second_data = second_data.transpose()

    for index, row in first_data.iterrows():
        val = row.values
        secVal = second_data.loc[:, index].values
        if(np.array_equiv(val, secVal)):
            results.append(fisher_z(1))
            ind.append(index)
        elif(len(np.unique(val)) > 1 and len(np.unique(secVal)) > 1):
            results.append(fisher_z(sc.pearsonr(val, secVal)[0]))
            ind.append(index)
        else:
            data_loss += 1
    results = pd.Series(results, index=ind)
    return results, data_loss


# calculatates the average of the fisher z transformed coefficients and reverse fisher z transforms it
# input corrdf should always be a dataframe of correlations
def get_average_corr(corrdf: pd.DataFrame) -> complex:
    return np.tanh(corrdf.mean())


def get_weighted_average_corr(corrdf: pd.DataFrame) -> complex:
    df = corrdf.value_counts().rename_axis(
        'unique_values').reset_index(name='counts')
    weights = df['counts']
    vals = df['unique_values']
    return (vals * weights).sum() / weights.sum()

def inf_to_real(num: complex) -> float:
    return float(num.real + num.imag)

def independent_correlation_test(corr1, corr2, n1, n2):
    return (corr1 - corr2) / np.sqrt((1 / (n1 - 3)) + (1 / (n2 - 3)))

def loss_calc(loss, other):
    total = loss + len(other)
    perc = np.round((loss / total) * 100)
    return loss, total, perc
