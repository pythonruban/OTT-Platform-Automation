import pandas as pd

def check_missing_flows(product_excel, testcase_excel):
    product_df = pd.read_excel(product_excel)
    testcase_df = pd.read_excel(testcase_excel)

    missing_flows = []
    for flow in product_df['Flow']:
        if flow not in list(testcase_df['TestCaseFlow']):
            missing_flows.append(flow)

    return missing_flows