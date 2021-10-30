import numpy as np
import pandas as pd


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
    corr = first_data.corrwith(second_data, axis)
    if(replace == True):
        corr = corr.replace(np.nan, 0)
    return corr.apply(fisher_z)


# calculatates the average of the fisher z transformed coefficients and reverse fisher z transforms it
# input corrdf should always be a dataframe of correlations
def get_average_corr(corrdf: pd.DataFrame) -> complex:
    return np.tanh(corrdf.mean())

def inf_to_real(num: complex) -> float:
    return float(num.real + num.imag)

def independent_correlation_test(corr1, corr2, n1, n2):
    return (corr1 - corr2) / np.sqrt((1 / (n1 - 3)) + (1 / (n2 -3)))
