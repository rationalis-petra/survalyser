# import pandas as pd
# import numpy as np
import lifelines as life
import numpy as np


class KaplanResult:
    def __init__(self):
        self.fitters = {}
        self.data = None


def update_eventcol(data, ecol, event_col):
    if ecol.dtypes == np.dtype('object'):
        mydict = {
            'True': True,
            'true': True,
            't': True,
            'T': True,
            'False': False,
            'false': False,
            'f': False,
            'F': False}
        return data.replace({event_col: mydict})[event_col]
    elif ecol.dtypes == np.dtype('int64'):
        return ~(data[event_col] == 0)
    else:
        print(ecol.dtypes)


def get_kaplan(data, time_col, event_col, discriminator_col):
    # step 1: find out all unique values for discriminator

    tcol = data[time_col]
    ecol = data[event_col]
    dcol = data[discriminator_col]

    cat = dcol.unique()

    ecol = update_eventcol(data, ecol, event_col)

    # step 2: create fitters for each value & fit data
    fitters = KaplanResult()
    for val in cat:
        fitter = life.KaplanMeierFitter()
        fitters.fitters[val] = fitter
        selector = dcol == val
        print(len(tcol[selector]))
        print(len(ecol[selector]))
        fitter.fit(tcol[selector],
                   ecol[selector],
                   label=val)

    # plt = life.plotting.add_at_risk_counts(kmf_indig,
    #                                        kmf_nonindig,
    #                                        ax=ax)
    fitters.data = (tcol,
                    ecol,
                    dcol,
                    cat)
    return fitters


def get_cox(data, tc, ec, value_cols):
    cols = value_cols
    cols.append(ec)
    cols.append(tc)
    data = data[cols]
    data[ec] = update_eventcol(data, data[ec], ec)
    print(data.columns)

    cph = life.CoxPHFitter()
    cph.fit(data, duration_col=tc, event_col=ec)

    return cph
