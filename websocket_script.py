import json
import requests
import websocket
import tkinter as tk
import login
import threading

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

# Make the WebSocket URL request
url = f"https://{server_name}/api/v1/{tenant_name}/me/websocket/"
response = requests.post(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Retrieve the WebSocket URL from the response
    websocket_url = response.json()["object"]

    # Create a set to store unique callIds
    call_ids = set()

    def on_message(ws, message):
        # Process the received event data here
        event = json.loads(message)
        event_type = event.get("notificationType")
        if event_type:
            # Extract the required data
            notification = event["notification"]
            call_id = notification.get("callId")
            callee_commonName = notification.get("calleePhoneNumber")
            caller_phone_number = notification.get("callerPhoneNumber")
            duration = notification.get("duration")

            # Check if the callId is already in the set
            if call_id not in call_ids:
                # Add the callId to the set
                call_ids.add(call_id)

                # Display the filtered information in the text widget
                filtered_info = f"Event Type: {event_type}\n"
                filtered_info += f"Callee Phone Number: {callee_commonName}\n"
                filtered_info += f"Caller Phone Number: {caller_phone_number}\n"
                filtered_info += f"Duration (minutes): {duration}\n\n"


                text_widget.insert(tk.END, filtered_info)
                text_widget.see(tk.END)

    def on_open(ws):
        # Define the event subscription requests
        subscription_requests = [
            {
                "messageType": "notificationRequest",
                "notificationType": "test",
                "toggle": True
            },
            {
                "messageType": "notificationRequest",
                "notificationType": "newCallEvent",
                "toggle": True
            },
            {
                "messageType": "notificationRequest",
                "notificationType": "callConnectedEvent",
                "toggle": True
            },
            {
                "messageType": "notificationRequest",
                "notificationType": "callHungUpEvent",
                "toggle": True
            },
            {
                "messageType": "notificationRequest",
                "notificationType": "missedCallEvent",
                "toggle": True
            },
            {
                "messageType": "notificationRequest",
                "notificationType": "channelHungUpEvent",
                "toggle": True
            },
            {
                "messageType": "notificationRequest",
                "notificationType": "callTransferredEvent",
                "toggle": True
            }
            # Add more subscription requests as needed
        ]

        # Send subscription requests
        for request in subscription_requests:
            ws.send(json.dumps(request))

    # Create a Tkinter window
    window = tk.Tk()
    window.title("Event Notifications")

    # Create a Text widget to display event messages
    text_widget = tk.Text(window, width=80, height=30)
    text_widget.pack()

    # Create a WebSocket connection
    ws = websocket.WebSocketApp(websocket_url, on_message=on_message, on_open=on_open)

    def start_websocket_connection():
        # Start the WebSocket connection
        ws.run_forever()

    # Start the WebSocket connection in a separate thread
    websocket_thread = threading.Thread(target=start_websocket_connection)
    websocket_thread.start()

    # Main Tkinter event loop
    window.mainloop()
else:
    print(f"Failed to retrieve WebSocket URL. Status code: {response.status_code}")
