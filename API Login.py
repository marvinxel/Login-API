import requests
import json
from tkinter import messagebox, Tk, Label, Entry, Button
from PIL import Image, ImageTk
import tkinter as tk


def login(username, password, user_space, tenant_name, server_name):
    url = f'https://{server_name}/api/v1/{tenant_name}/me/login'
    payload = {
        'userName': username,
        'password': password,
        'userSpace': user_space
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        response_json = response.json()
        response_json['serverName'] = server_name
        response_json['tenantName'] = tenant_name
        return response_json

    return None


def set_placeholder_opacity(entry, event):
    if event.type == "9":
        # Focus in event
        if entry.get() == "":
            entry.configure(fg="#000000")  # Set text color to black
    elif event.type == "10":
        # Focus out event
        if entry.get() == "":
            entry.configure(fg="#7f7f7f")  # Set text color to grey


def on_login_button_click():
    username = username_entry.get()
    password = password_entry.get()
    server_name = server_name_entry.get()
    tenant_name = tenant_name_entry.get()

    # Get the response from the login API
    authentication = login(username, password, '', tenant_name, server_name)

    if authentication:
        try:
            with open("login.py", "w") as login_file:
                login_file.write(f'response = \'{json.dumps(authentication)}\'\n')
                login_file.write(f'servername = \'{server_name}\'\n')
                login_file.write(f'tenant = \'{tenant_name}\'\n')

            messagebox.showinfo("Inloggen", "Inloggen is gelukt!")
            window.destroy()  # Hide the login screen upon successful login
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update login.py: {str(e)}")
    else:
        messagebox.showerror("Inloggen", "Inloggen is mislukt!")



# Create a Tkinter window
window = Tk()
window.title("Inlog Scherm")

# Load the logo image
logo_image = Image.open("xelion_logo.png")
# Resize the logo image to a smaller size
logo_image = logo_image.resize((200, 200))  # Adjust the dimensions as per your requirement

# Create a PhotoImage object from the resized logo image
logo_photo = ImageTk.PhotoImage(logo_image)

# Create a label to display the logo
logo_label = tk.Label(window, image=logo_photo)
logo_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")

# Create labels and entries for username, password, server name, and tenant name
Label(window, text="Gebruikersnaam:").grid(row=1, column=1, padx=10, pady=5)
username_entry = Entry(window, fg="#7f7f7f", highlightthickness=0)
username_entry.grid(row=1, column=2)
username_entry.bind("<FocusIn>", lambda event: set_placeholder_opacity(username_entry, event))
username_entry.bind("<FocusOut>", lambda event: set_placeholder_opacity(username_entry, event))

Label(window, text="Wachtwoord:").grid(row=2, column=1, padx=10, pady=5)
password_entry = Entry(window, show="*", fg="#7f7f7f", highlightthickness=0)
password_entry.grid(row=2, column=2)
password_entry.bind("<FocusIn>", lambda event: set_placeholder_opacity(password_entry, event))
password_entry.bind("<FocusOut>", lambda event: set_placeholder_opacity(password_entry, event))

Label(window, text="Server Naam:").grid(row=3, column=1, padx=10, pady=5)
server_name_entry = Entry(window, fg="#7f7f7f", highlightthickness=0)
server_name_entry.grid(row=3, column=2)
server_name_entry.bind("<FocusIn>", lambda event: set_placeholder_opacity(server_name_entry, event))
server_name_entry.bind("<FocusOut>", lambda event: set_placeholder_opacity(server_name_entry, event))

Label(window, text="Tenant Naam:").grid(row=4, column=1, padx=10, pady=5)
tenant_name_entry = Entry(window, fg="#7f7f7f", highlightthickness=0)
tenant_name_entry.grid(row=4, column=2)
tenant_name_entry.bind("<FocusIn>", lambda event: set_placeholder_opacity(tenant_name_entry, event))
tenant_name_entry.bind("<FocusOut>", lambda event: set_placeholder_opacity(tenant_name_entry, event))


# Create a login button
Button(window, text="Inloggen", command=on_login_button_click).grid(row=5, column=1, columnspan=2, pady=10)

# Add an empty row
Label(window, text="").grid(row=6)

# Run the Tkinter event loop
window.mainloop()
