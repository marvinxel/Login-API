import requests
import json
import login  #Assuming login.py contains the necessary credentials

#Read line OIDs from lineoids.txt
with open('lineoids.txt', 'r') as f:
    line_oids = f.read().splitlines()

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
url = f"https://{server_name}/api/v1/{tenant_name}/phonelines/{{}}"

response = requests.get(url, headers=headers)
# List to store line information
lineinformation = []

# Default empty list for forwardCallerIdMap
forward_caller_id_map = []

# Iterate over line OIDs
for oid in line_oids:
    try:
        # Make GET request to retrieve line data
        response = requests.get(url.format(oid), headers=headers)
        response.raise_for_status()
        data = response.json()

        # Extract desired information from the response
        user_phone_line = data["object"].get("userPhoneLine", {})
        forward_caller_id_map = data["object"].get("forwardCallerIdMap", [])
        auto_attendant_on = data["object"].get("autoAttendantOn", False)
        auto_attendant_actions = []

        # Check if auto attendant is enabled and collect action details
        if auto_attendant_on:
            for i in range(1, 10):
                action_name = f"action{i}"
                if action_name in data["object"]["autoAttendant"]:
                    action = data["object"]["autoAttendant"][action_name]
                    auto_attendant_actions.append(action)

        line_data = {
            "External Number": data["object"]["externalNumber"],
            "Caller Name": data["object"]["callerName"],
            "Extensions": [ext["commonName"] for ext in data["object"]["extensions"]],
            "Users": [user["user"]["person"]["commonName"] for user in data["object"]["users"]],
            "Day/Night Mode": data["object"].get("dayNightMode", {}).get("enableDayNightMode", False),
            "Max Queue Length": data["object"].get("maxQueueLength", 0),
            "Fallback Common Name": data["object"].get("defaultFallback", {}).get("commonName", ""),
            "Fallback OID": data["object"].get("defaultFallback", {}).get("oid", ""),
            "Timeout": user_phone_line.get("timeout", 0),
            "Do Not Disturb": user_phone_line.get("doNotDisturb", False),
            "Forward Caller ID Map": {
                "Address Start": forward_caller_id_map[0]["addressStart"] if forward_caller_id_map else "",
                "Transfer Line": forward_caller_id_map[0]["transferLine"]["commonName"] if forward_caller_id_map and forward_caller_id_map[0].get("transferLine") else ""
            },
            "commonName": data["object"]["commonName"],
            "Line OID": oid,
            "Auto Attendant On": auto_attendant_on,
            "Auto Attendant Actions": auto_attendant_actions
        }

        # Append line data to the list
        lineinformation.append(line_data)

    except requests.exceptions.HTTPError as err:
        print(f"Failed to retrieve data for OID: {oid}. Error: {err}")

# Write line information to a new file called Line Information
with open('lineinformation.txt', 'w') as f:
    json.dump(lineinformation, f, indent=4)

print("Line information has been written to lineinformation.txt.")
