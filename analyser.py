# import pandas as pd
# import numpy as np
import lifelines as life


def get_kaplan(data, time_col, event_col, discriminator_col):
    # step 1: find out all unique values for discriminator
    cat = data[discriminator_col].unique()

    # step 2: create fitters for each value & fit data
    fitters = {}
    for val in cat:
        fitter = life.KaplanMeierFitter()
        fitters[val] = fitter
        selector = data[discriminator_col] == val
        fitter.fit(data.loc[selector, time_col],
                   data.loc[selector, event_col],
                   label=val)

    # step 3: plot the data
    # TODO: title
    ax = None
    for (val, fitter) in fitters.items():
        ax = fitter.plot(ci_show=False,
                         xlim=(0, 20),
                         ax=ax)

    # plt = life.plotting.add_at_risk_counts(kmf_indig,
    #                                        kmf_nonindig,
    #                                        ax=ax)
    return ax.get_figure()


def get_cox(data, tc, ec, value_cols):
    print(tc)
    print(ec)
    print(value_cols)

    cols = value_cols
    cols.append(ec)
    cols.append(tc)
    data = data[cols]
    print(data.columns)

    cph = life.CoxPHFitter()
    cph.fit(data, duration_col=tc, event_col=ec)

    out = cph.plot()
    out.get_figure().savefig("test-data/test-cph.png")

    return cph
