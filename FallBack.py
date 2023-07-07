import json
from graphviz import Digraph

# Load line information from the file
with open("lineinformation.json", "r") as f:
    line_information = json.load(f)

# Create a new Digraph
graph = Digraph()

# Recursive function to add nodes and edges
def add_extension_and_fallback(extension, parent_extension=None):
    extension_number = extension["Extensions"][0] if extension["Extensions"] else ""
    fallback_oid = extension["Fallback OID"]
    common_name = extension["commonName"]

    # Add node for the extension
    graph.node(extension_number, label=f"{extension_number}\n{common_name}", shape="box")

    # Connect the extension with its parent extension
    if parent_extension:
        graph.edge(parent_extension, extension_number)

    # Check if there is a fallback
    if fallback_oid:
        fallback = next((line for line in line_information if line["Line OID"] == fallback_oid), None)
        if fallback:
            add_extension_and_fallback(fallback, extension_number)  # Recursive call to handle fallback

# Find the main lines (extensions starting with "+31")
main_lines = [line for line in line_information if line["Extensions"] and line["Extensions"][0].startswith("+31")]

# If main lines exist, start adding extensions and fallbacks
if main_lines:
    for main_line in main_lines:
        add_extension_and_fallback(main_line)

# Render and save the workflow diagram
graph.render("workflow_diagram", format="png", cleanup=True)
