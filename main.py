import requests
import json
import csv

url = "https://services.chipotle.com/restaurant/v3/restaurant"

payload = json.dumps({
  "latitude": 37.687176099999974,
  "longitude": -97.33005299999998,
  "radius": 9999999,
  "restaurantStatuses": [
    "OPEN",
    "CLOSED",
    "LAB"
  ],
  "conceptIds": [
    "CMG"
  ],
  "orderBy": "distance",
  "orderByDescending": False,
  "pageSize": 4000,
  "pageIndex": 0,
  "embeds": {
    "addressTypes": [
      "MAIN"
    ],
    "realHours": True,
    "directions": True,
    "catering": True,
    "onlineOrdering": True,
    "timezone": True,
    "marketing": True,
    "chipotlane": True,
    "sustainability": True,
    "experience": True
  }
})
headers = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.9',
  'Chipotle-CorrelationId': 'OrderWeb-5086225b-dda3-4183-b149-b27708003835',
  'Connection': 'keep-alive',
  'Content-Type': 'application/json',
  'Ocp-Apim-Subscription-Key': 'b4d9f36380184a3788857063bce25d6a',
  'Origin': 'https://chipotle.com',
  'Referer': 'https://chipotle.com/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-site',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'Cookie': 'f5avraaaaaaaaaaaaaaaa_session_=MOINFLDGJEGCKANOKBGGIACCJJLBPOHINEHHJIFHAGDAPHKBBGKGBKMMDKNMEHKEOKADEOKNEDBILJKIFIDAKEKDIBILLNLDBCFKLKBLAELALFMCDBMELIBODOKIFFLK; TS01cfe0ce=0106a0d561d2315d1f5b70f13e6e6673a4cfcb85e4a90cc3be7b14db63fc71bcb18453e894a6e2fc66d95a0ea8afaf11ece6032c9e720cd0acb22b0add9265a2893f4f1db9'
}

response = requests.request("POST", url, headers=headers, data=payload)
stores = json.loads(response.text)

print(json.dumps(stores, indent=4))

def parse_address(address_json):
    def safe_get(dictionary, key):
        return dictionary.get(key, "")

    if len(address_json) < 1:
        return ""
    address = address_json[0]

    # Construct the address string
    address_str = f"{safe_get(address, 'addressLine1')} {safe_get(address, 'addressLine2').strip()} {safe_get(address, 'locality')}, {safe_get(address, 'administrativeArea')} {safe_get(address, 'postalCode')} {safe_get(address, 'countryCode')}".strip()

    return address_str

def parse_store_hours(hours_json):
    hours_string = ""
    for day in hours_json:
        day_of_week = day.get("dayOfWeek", "Day")
        open_time = day.get("openDateTime", "Open Time").split("T")[1]
        close_time = day.get("closeDateTime", "Close Time").split("T")[1]
        hours_string += f"{day_of_week}: {open_time} - {close_time}\n"
    return hours_string.strip()

with open('ChipotleLocations.csv', mode='w') as CSVFile:
    writer = csv.writer(CSVFile, delimiter=",")

    writer.writerow([
        "restaurantNumber",
        "restaurantName", 
        "address", 
        "storeHours"
    ])

    for store in stores['data']:
        row = []
        store_id = store["restaurantNumber"]
        store_name = store["restaurantName"]
        try:
            address = parse_address(store["addresses"])
        except Exception as e:
            print("Could not parse address: ", e)

        try:
            store_hours = parse_store_hours(store["realHours"])
        except Exception as e:
            print("Could not parse store hours: ", e)

        row.append(store_id)
        row.append(store_name)
        row.append(address)
        row.append(store_hours)
        
        writer.writerow(row)