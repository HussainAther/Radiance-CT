import logging
import pandas as pd

def log_clinical_session(epoch, loss, dcr, category):
    data = {
        "epoch": [epoch],
        "loss": [loss],
        "dcr": [dcr],
        "birads_category": [category]
    }
    df = pd.DataFrame(data)
    # Append to a master clinical log for Dick to review
    df.to_csv("outputs/reports/clinical_log.csv", mode='a', header=False, index=False)
