import pandas as pd
import numpy as np
import lifelines as life


def get_dataframe(filename):
    print("using stub get_dataframe")

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

    # remove problematic_patients
    data = data[~np.isnan(data["brca-time"])]
    data["brca-time"] = data["brca-time"].apply(to_days)
    data["brca-time"] = data["brca-time"] / 365.25

    return data


def to_days(time):
    return time.days


def analysis_demo():
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
    kmf = life.KaplanMeierFitter()
    kmf.fit(data.loc[indig_series, "brca-time"],
            data.loc[indig_series, "brca-event"],
            label="Indigenous")

    # we can easily plot the survival curve as well
    # we set ci_show = False to hide confidence intervals
    res = kmf.plot(ci_show=False,
                   title="Indigeous Survival",
                   xlim=(0, 20),
                   ylim=(0, 1),
                   at_risk_counts=True)

    out = kmf.plot(ci_show=False, ax=res, at_risk_counts=True, xlim=(0, 20))

    out.get_figure().savefig("test-data/test.png")
