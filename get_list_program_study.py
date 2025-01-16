import requests
import json

# URL of the page with the dropdown (you may need to adjust this for pagination)
base_url = 'https://api-sscasn.bkn.go.id/2024/referensi/pendidikan'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Referer': 'https://sscasn.bkn.go.id/',
    'Origin': 'https://sscasn.bkn.go.id',
}

# Parameters
limit = 2500  # maximum per page
max_data = 400  # desired total data
all_data = []  # list to store all the data
page = 1  # start from page 1

# Fetch data in pages until you reach the max_data or run out of data
while len(all_data) < max_data:
    # Construct the request URL with pagination (limit and offset)
    params = {
        'tingkat': 40,
        'nama': 'null',
        'limit': limit,
        'offset': (page - 1) * limit  # calculate offset based on the page number
    }
    
    # Send the request
    response = requests.get(base_url, headers=headers, params=params)
    
    # Check if the response is valid
    if response.status_code == 200:
        # Get the response JSON data
        data = response.json()
        
        # Extract the 'data' field from the response
        if 'data' in data and 'data' in data['data']:
            # Append the current page data to the all_data list
            all_data.extend(data['data']['data'])
            
            # Check if we've reached or exceeded the desired amount of data
            if len(all_data) >= max_data:
                break
        else:
            print("Unexpected structure in response.")
            break
    else:
        print(f"Error: Unable to fetch data from the API (status code: {response.status_code})")
        break
    
    # Increment page to fetch the next set of data
    page += 1

# At this point, all_data contains all the collected data
print(f"Collected {len(all_data)} items.")

# Prepare the data for JSON output in the desired format
programs_dict = {}
for item in all_data:
    program_name = item['nama_pend'].lower().replace(' ', '_')  # Convert to lowercase and replace spaces with underscores
    programs_dict[program_name] = {
        'kode': item['kode_pend'],
        'nama_pendidikan': item['nama_pend']
    }

# Save the data to kode_ref_pend.json
with open('kode_ref_pend.json', 'w', encoding='utf-8') as json_file:
    json.dump(programs_dict, json_file, ensure_ascii=False, indent=4)

print("Data saved to kode_ref_pend.json.")
