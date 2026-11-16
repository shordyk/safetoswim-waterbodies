import requests
import pandas as pd
from pathlib import Path

# WGP Web Services API: https://www.waterqualitydata.us/webservices_documentation/
# User Guide: https://www.waterqualitydata.us/portal_userguide/
# SETTINGS

base_url = "https://www.waterqualitydata.us/data/Result/search?"

start_date = "01-01-1970"
end_date = "12-31-2020"

out_dir = Path(r"C:\Users\SHordyk\Desktop\safetoswim-waterbodies\data\raw")
out_dir.mkdir(exist_ok=True)

characteristics = [
    "Chloride",
    "Specific conductance",
    "Salinity",
    #other names for salinity?
]

##### Download #####

params = { 
    "statecode": "US:06", # California
    "sampleMedia": "Water",
    "characteristicName": ";".join(characteristics), #Documentation says seperated by semicolon
    "startDateLo": start_date,
    "startDateHi": end_date,
    "mimeType": "csv",
    "zip": "yes",
    "dataProfile": "resultPhysChem", #To check name, had it generate a url on the beta tool 
}


print("Downloading WQP data from NWIS...")
print("Characteristics:", characteristics)

try:
    response = requests.get(base_url, params=params, timeout=300)
    response.raise_for_status()
except requests.exceptions.Timeout:
    print("Request timed out — server didn't respond in time.")
    raise
except requests.exceptions.HTTPError:
    print("Status:", response.status_code)
    print("Body:", response.text[:2000])
    raise

response.raise_for_status()

print("Download complete. Saving to file...")
print("HTTP status code:", response.status_code)


##### SAVING #####
zip_path = out_dir / "wqp_data_raw.zip"

with open(zip_path, "wb") as f:
    f.write(response.content)

print("Saved to:", zip_path)
