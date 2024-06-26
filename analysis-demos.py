import pandas as pd
import numpy as np
import lifelines as life


def to_days(time):
    return time.days


def kaplan_demo():
    indigenous_survival = pd.read_csv("test-data/indigenous-survival.csv")
    indigenous_factors = pd.read_csv("test-data/indigenous-data.csv")

    # EXTENSION
    # MERGE
    raw_data = pd.merge(indigenous_survival,
                        indigenous_factors,
                        on="ATSI_DB_ID")

    # EXTENSION
    # REFINE
    data = raw_data[raw_data["Elig adj surv"] == 1]

    # EXTENSION
    # COL SELECT & RENAME

    data = data[[
        "ATSI_DB_ID", "EarliestDxDate", "1_DoR", "FU_StatusDate", "DOD",
        "CODTYPE", "Indignous/NonIndigenous", "BiolSubtype", "DxARIA3",
        "IRSD_Score", "IRSAD_Score", "IER_Score", "IEO_Score", "Grade",
        "Age Dx"
    ]]

    data.columns = [
        "id", "date-dx", "date-relapse", "date-fu", "date-death",
        "cause-death", "indigenous?", "subtype", "aria3", "irsd", "irsad",
        "ier", "ieo", "grade", "age-dx"
    ]

    # EXTENSION
    # Time Calc
    data["date-fu"] = pd.to_datetime(data["date-fu"])
    data["date-death"] = pd.to_datetime(data["date-death"])
    data["date-dx"] = pd.to_datetime(data["date-dx"])

    data["brca-event"] = data["cause-death"] == "C-BrCa"
    data["brca-time"] = data["date-fu"] - data["date-dx"]

    data = data[~np.isnan(data["brca-time"])]

    data["brca-time"] = data["brca-time"].apply(to_days)
    data["brca-time"] = data["brca-time"] / 365.25

    indig_series = data["indigenous?"] == "Indigenous"
    kmf_indig = life.KaplanMeierFitter()
    kmf_nonindig = life.KaplanMeierFitter()
    kmf_indig.fit(data.loc[indig_series, "brca-time"],
                  data.loc[indig_series, "brca-event"],
                  label="Indigenous")
    kmf_nonindig.fit(data.loc[~indig_series, "brca-time"],
                     data.loc[~indig_series, "brca-event"],
                     label="Non Indigenous")

    # we can easily plot the survival curve as well
    # we set ci_show = False to hide confidence intervals
    res = kmf_indig.plot(ci_show=False,
                         title="Indigeous Survival",
                         xlim=(0, 20),
                         ylim=(0, 1),
                         at_risk_counts=False)
    res = kmf_indig.plot(ci_show=False,
                         ax=res,
                         at_risk_counts=False)

    plt = life.plotting.add_at_risk_counts(kmf_indig,
                                           kmf_nonindig,
                                           ax=res)

    plt.get_figure().savefig("test-data/test-kaplan.png")


def cox_demo():
    indig = pd.read_csv("test-data/indigenous-clean.csv")
    indig = indig[['aria3', 'brca-event', 'brca-time']]
    cph = life.CoxPHFitter()
    cph.fit(indig, duration_col="brca-time", event_col="brca-event")

    # print
    cph.print_summary()

    out = cph.plot()
    out.get_figure().savefig("test-data/test-cph.png")
