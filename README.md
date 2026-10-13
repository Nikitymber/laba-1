import requests
import pandas as pd
import xml.etree.ElementTree as ET

date_start = "01/01/2025"
date_end = "13/10/2026"

currencies = {
    "USD": "R01235",
    "EUR": "R01239",
    "CNY": "R01375"
}

session = requests.Session()
session.trust_env = False

dfs = []

for currency, currency_id in currencies.items():

    url = "http://www.cbr.ru/scripts/XML_dynamic.asp"

    params = {
        "date_req1": date_start,
        "date_req2": date_end,
        "VAL_NM_RQ": currency_id
    }

    response = session.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    root = ET.fromstring(response.content)

    data = []

    for record in root.findall("Record"):

        date = pd.to_datetime(
            record.attrib["Date"],
            format="%d.%m.%Y"
        )

        nominal = float(
            record.findtext("Nominal").replace(",", ".")
        )

        value = float(
            record.findtext("Value").replace(",", ".")
        )

        data.append({
            "date": date,
            currency: value / nominal
        })

    dfs.append(pd.DataFrame(data).set_index("date"))

rates_df = pd.concat(dfs, axis=1).sort_index()

print(rates_df.tail())
