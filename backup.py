import requests
import pandas as pd

base_url = 'https://api-sscasn.bkn.go.id/2024/portal/spf?kode_ref_pend=5110120&pengadaan_kd=3&offset=0'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Referer' : 'https://sscasn.bkn.go.id/',
    'Origin' : 'https://sscasn.bkn.go.id',
}

all_data = []
offset = 0
items_per_page = 10
max_data = 10000

while offset < max_data:
    url = f'{base_url}{offset}'
    print(f"Requestiong data from URL: {url}")
a
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        break
    try:
        response_son = response.json()
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Response content: {response.text}")
        break

    if 'data' in response_son and 'data' in response_son['data']:
        data = response_son['data']['data']
        all_data.extend(data)
        offset += items_per_page
    else:
        print("No more data Available")
        break

df = pd.DataFrame(all_data)
df.to_csv('sscasn_data.csv', index=False)
print("Data has been successfully saved to data.csv")