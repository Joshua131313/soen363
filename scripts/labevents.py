import pandas as pd

def load_labevents_dict():
    raw_df = pd.read_csv(
        "../csv_tables/LABEVENTS_random.csv",
        dtype=str,
        low_memory=False,
    )

    column_map = {
        "ROW_ID": "row_id",
        "SUBJECT_ID": "patient_id",
        "HADM_ID": "admission_id",
        "ITEMID": "item_id",
        "CHARTTIME": "chart_time",
        "VALUE": "value",
        "VALUENUM": "value_num",
        "VALUEUOM": "value_unit",
        "FLAG": "flag"
    }

    raw_df.rename(columns=column_map, inplace=True)

    return raw_df.to_dict(orient="records")
