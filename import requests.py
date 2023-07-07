import json
import sys
import requests
from PIL import Image, ImageTk
import login  # Assuming login.py contains the necessary credentials

# Retrieve the server name and tenant name from the login process
server_name = login.servername
tenant_name = login.tenant

# Retrieve the access_token from the response
response_data = json.loads(login.response)
access_token = response_data["authentication"]

# Set the headers and access token
headers = {
    "Content-Type": "application/json",
    "Authorization": "xelion " + access_token
}

# Make the API request
url = f"https://{server_name}/api/v1/{tenant_name}/phonelines?limit=200"
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    line_oids = [line["object"]["oid"] for line in data["data"]]

    # Write line OIDs to the text file
    with open("lineoids.txt", "w") as file:
        file.write("\n".join(line_oids))
        print("Line OIDs have been updated in lineoids.txt.")
else:
    print(f"Failed to retrieve line OIDs. Status code: {response.status_code}")
