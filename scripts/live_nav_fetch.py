import requests
import pandas as pd

schemes = {
    "HDFC Top 100":125497,
    "SBI Bluechip":119551,
    "ICICI Bluechip":120503,
    "Nippon Large Cap":118632,
    "Axis Bluechip":119092,
    "Kotak Bluechip":120841
}

rows = []

for name, code in schemes.items():

    url = f"https://api.mfapi.in/mf/{code}"

    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()

        rows.append({
            "scheme_name": name,
            "scheme_code": code,
            "latest_nav": data["data"][0]["nav"],
            "date": data["data"][0]["date"]
        })

df = pd.DataFrame(rows)

df.to_csv("data/raw/live_nav.csv", index=False)

print(df)
