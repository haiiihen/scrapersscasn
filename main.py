import requests
import pandas as pd
import json
import time
from http.client import RemoteDisconnected

# Load kode_ref_pend from the external JSON file
with open('kode_ref_pend.json', 'r') as f:
    kode_ref_pend = json.load(f)

# base_url_template = 'https://api-sscasn.bkn.go.id/2024/portal/spf?kode_ref_pend={}&instansi_id=A5EB03E23B43F6A0E040640A040252AD&pengadaan_kd=2&offset={}'
base_url_template = 'https://api-sscasn.bkn.go.id/2024/portal/spf?kode_ref_pend={}&pengadaan_kd=2&offset={}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Referer': 'https://sscasn.bkn.go.id/',
    'Origin': 'https://sscasn.bkn.go.id',
}

all_data = []
items_per_page = 10  # Assuming each page has 10 items

def fetch_data_with_retries(url, headers, retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx/5xx)
            return response.json()  # Return the JSON data if successful
        except (requests.exceptions.RequestException, RemoteDisconnected) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)  # Wait before retrying
            delay *= 2  # Exponentially increase the delay
    print("All attempts failed.")
    return None  # Return None if all retries fail

# Loop over the kode_ref_pend dictionary
for key, value in kode_ref_pend.items():
    kode = value['kode']
    nama_pendidikan = value['nama_pendidikan']
    
    print(f"Fetching data for {key} with kode_ref_pend = {kode}")

    offset = 0  # Reset the offset for each kode_ref_pend
    while True:
        url = base_url_template.format(kode, offset)
        print(f"Requesting data from URL: {url}")

        # Fetch data with retry logic
        response_json = fetch_data_with_retries(url, headers)
        if response_json is None:
            break  # If all retries fail, stop further requests

        # Check if the response contains data
        if 'data' in response_json and isinstance(response_json['data'], dict) and 'data' in response_json['data']:
            data = response_json['data']['data']
            
            if not data:  # If no data is returned, break the loop
                print("No more data available.")
                break

            for record in data:
                record_data = {
                    'kode_ref_pend': kode,  
                    'nama_pendidikan': nama_pendidikan,  
                    **record  
                }
                all_data.append(record_data)

            offset += items_per_page
        else:
            print("Error: Data not found in the response.")
            break

        time.sleep(1)  # Add a small delay between requests

# Convert the collected data to a DataFrame for easier inspection
df = pd.DataFrame(all_data)
df.to_csv('sscasn_data_s1_teknik_informatika.csv', index=False)
print(df)
