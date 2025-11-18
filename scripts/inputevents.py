import pandas as pd

def load_inputevents_cv_dict():
    raw_input_df = pd.read_csv(
        "../csv_tables/INPUTEVENTS_CV_random.csv",
        dtype=str,           
        low_memory=False      
    )

    cleaned_input_df = raw_input_df[[
        'ROW_ID', 'SUBJECT_ID', 'HADM_ID', 'ICUSTAY_ID',
        'CHARTTIME', 'ITEMID', 'AMOUNT', 'AMOUNTUOM',
        'RATE', 'RATEUOM', 'STORETIME', 'CGID',
        'ORDERID', 'LINKORDERID', 'STOPPED', 'NEWBOTTLE',
        'ORIGINALAMOUNT', 'ORIGINALAMOUNTUOM',
        'ORIGINALROUTE', 'ORIGINALRATE', 'ORIGINALRATEUOM',
        'ORIGINALSITE'
    ]].copy()

    column_map = {
        'ROW_ID': 'row_id',
        'SUBJECT_ID': 'patient_id',
        'HADM_ID': 'admission_id',
        'ICUSTAY_ID': 'icu_stay_id',
        'CHARTTIME': 'chart_time',
        'ITEMID': 'item_id',
        'AMOUNT': 'amount',
        'AMOUNTUOM': 'amount_unit',
        'RATE': 'rate',
        'RATEUOM': 'rate_unit',
        'STORETIME': 'store_time',
        'CGID': 'caregiver_id',
        'ORDERID': 'order_id',
        'LINKORDERID': 'link_order_id',
        'STOPPED': 'stopped',
        'NEWBOTTLE': 'new_bottle',
        'ORIGINALAMOUNT': 'original_amount',
        'ORIGINALAMOUNTUOM': 'original_amount_unit',
        'ORIGINALROUTE': 'original_route',
        'ORIGINALRATE': 'original_rate',
        'ORIGINALRATEUOM': 'original_rate_unit',
        'ORIGINALSITE': 'original_site'
    }

    cleaned_input_df.rename(columns=column_map, inplace=True)
    return cleaned_input_df.to_dict(orient="records")
