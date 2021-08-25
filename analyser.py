# import pandas as pd
# import numpy as np
import lifelines as life


class KaplanResult:
    def __init__(self):
        self.fitters = {}
        self.data = None


def get_kaplan(data, time_col, event_col, discriminator_col):
    # step 1: find out all unique values for discriminator
    cat = data[discriminator_col].unique()

    # step 2: create fitters for each value & fit data
    fitters = KaplanResult()
    for val in cat:
        fitter = life.KaplanMeierFitter()
        fitters.fitters[val] = fitter
        selector = data[discriminator_col] == val
        fitter.fit(data.loc[selector, time_col],
                   data.loc[selector, event_col],
                   label=val)

    # plt = life.plotting.add_at_risk_counts(kmf_indig,
    #                                        kmf_nonindig,
    #                                        ax=ax)
    fitters.data = (data[time_col],
                    data[event_col],
                    data[discriminator_col],
                    cat)
    return fitters


def get_cox(data, tc, ec, value_cols):
    cols = value_cols
    cols.append(ec)
    cols.append(tc)
    data = data[cols]
    print(data.columns)

    cph = life.CoxPHFitter()
    cph.fit(data, duration_col=tc, event_col=ec)

    return cph
