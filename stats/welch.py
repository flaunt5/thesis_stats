import numpy as np
from scipy.stats import t
import pandas as pd

# code copied from https://stats.stackexchange.com/questions/475289/confidence-interval-for-2-sample-t-test-with-scipy


def welch_ttest(x1, x2):

    n1 = x1.size
    n2 = x2.size
    m1 = np.mean(x1)
    m2 = np.mean(x2)

    v1 = np.var(x1, ddof=1)
    v2 = np.var(x2, ddof=1)

    pooled_se = np.sqrt(v1 / n1 + v2 / n2)
    delta = m1-m2

    tstat = delta / pooled_se
    df = (v1 / n1 + v2 / n2)**2 / \
        (v1**2 / (n1**2 * (n1 - 1)) + v2**2 / (n2**2 * (n2 - 1)))

    # two side t-test
    p = 2 * t.cdf(-abs(tstat), df)

    # upper and lower bounds
    lb = delta - t.ppf(0.975, df)*pooled_se
    ub = delta + t.ppf(0.975, df)*pooled_se

    return pd.DataFrame(np.array([tstat, df, p, delta, lb, ub]).reshape(1, -1),
                        columns=['T statistic', 'df', 'pvalue 2 sided', 'Difference in mean', 'lb', 'ub'])
