import matplotlib.pyplot as plt
import json
import matplotlib.patches as patches
from tkinter import messagebox

# Load line information from the file
with open("lineinformation.json", "r") as f:
    line_information = json.load(f)

# Create a figure and axis
fig, ax = plt.subplots()

# Create circles for each phone line
for i, line in enumerate(line_information):
    users = line["Users"]
    num_users = len(users)

    # Create a circle patch
    circle = patches.Circle((i, num_users), radius=0.5, edgecolor='black')

    # Add the circle to the plot
    ax.add_patch(circle)

    # Add the number of users as a label inside the circle
    ax.text(i, num_users, str(num_users), ha='center', va='center')

# Set the axis labels and title
ax.set_xlabel("Phone Line")
ax.set_ylabel("Number of Users")
ax.set_title("Users per Phone Line")

# Set the x-axis ticks and labels
line_names = [line.get("commonName", "Unknown") for line in line_information]
ax.set_xticks(range(len(line_information)))
ax.set_xticklabels(line_names, rotation=45, ha='right')

# Set the y-axis limits based on the maximum number of users
max_users = max(len(line["Users"]) for line in line_information)
ax.set_ylim(0, max_users + 1)

# Make the circles clickable
def on_circle_click(event):
    line_index = int(event.xdata)
    line = line_information[line_index]
    users = line["Users"]
    user_list = '\n'.join(users)
    messagebox.showinfo("Users Information", f"Users for line {line['commonName']}:\n{user_list}")

# Connect the click event handler to the figure
fig.canvas.mpl_connect('button_press_event', on_circle_click)

# Display the plot
plt.show()
