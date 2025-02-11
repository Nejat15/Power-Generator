import requests
from bs4 import BeautifulSoup
import tkinter as tk
import webbrowser

# Function to retrieve the random power, description, capabilities, and URL
def get_random_power():
    try:
        # Step 1: Get a random power page from the wiki
        url = "https://powerlisting.fandom.com/wiki/Special:Random"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Step 2: Extract the power name using the span class "mw-page-title-main"
        power_name = soup.find('span', {'class': 'mw-page-title-main'}).get_text(strip=True)

        # Step 4: Extract capabilities, checking for the <h2> with id "Capabilities"
        capabilities = "Capabilities not available"
        capabilities_section = soup.find('span', {'id': 'Capabilities'})
        
        if capabilities_section:
            capabilities_paragraph = capabilities_section.find_next('p')  # Get the first <p> after the h2
            if capabilities_paragraph:
                capabilities = capabilities_paragraph.get_text(strip=True)
            else:
                capabilities = "Capabilities not found."
        else:
            capabilities = "Capabilities section not available."

        # Get the current URL for the power
        power_url = response.url  # This gives us the URL of the current power page

        # Return the power, capabilities, and the URL (no description)
        return power_name, capabilities, power_url

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error", f"An error occurred: {e}", ""

# Function to open the webpage in the browser
def open_website():
    if current_url:
        webbrowser.open(current_url)

# Function to display a selected power from the history
def show_power_details(power_name):
    for p_name, p_cap, p_url in power_history:
        if p_name == power_name:
            power_label.config(text=p_name)
            capabilities_label.config(text=p_cap)
            global current_url
            current_url = p_url
            open_button.config(command=open_website)

# Global variables
current_url = ""
power_history = []

# Create a basic GUI to display the generated power and capabilities
def update_gui():
    global current_url
    power, capabilities, url = get_random_power()

    # Add the current power to history (keep last 10 powers)
    power_history.insert(0, (power, capabilities, url))
    if len(power_history) > 10:
        power_history.pop()

    # Set the labels with the fetched power details, without the "Power:" and "Capabilities:" labels
    power_label.config(text=power)
    capabilities_label.config(text=capabilities)

    # Store the URL for the current power
    current_url = url

    # Update the Open Website button to use the correct URL
    open_button.config(command=open_website)

    # Update history display
    update_history_display()

# Update the history section to show the last 10 powers
def update_history_display():
    # Clear only the history buttons (not the note label)
    for widget in history_frame.winfo_children():
        if isinstance(widget, tk.Button):
            widget.destroy()

    # Add the last 10 powers from the history
    for power, _, _ in power_history:
        power_button = tk.Button(history_frame, text=power, font=("Helvetica", 10), bg="#f0f8ff", anchor="w", padx=10, command=lambda p=power: show_power_details(p))
        power_button.pack(fill="x", pady=2)

# Setup Tkinter window
root = tk.Tk()
root.title("Power Generator")

# Disable window resizing (prevents maximizing)
root.resizable(False, False)

# Set a light background color
root.config(bg="#f0f8ff")

# Set font style
font_style = ("Helvetica", 12)

# Create the labels to display the power and capabilities (no description)
power_label = tk.Label(root, font=("Helvetica", 14, "bold"), bg="#f0f8ff", anchor="center", padx=10, wraplength=400)
power_label.pack(pady=5, fill="both", expand=True)

capabilities_label = tk.Label(root, font=font_style, bg="#f0f8ff", anchor="center", padx=10, wraplength=400)
capabilities_label.pack(pady=5, fill="both", expand=True)

# History frame
history_frame = tk.Frame(root, bg="#f0f8ff")
history_frame.pack(pady=10, fill="x")

history_note = tk.Label(history_frame, text="Last 10 Powers:", font=("Helvetica", 10), bg="#f0f8ff")
history_note.pack()

# Button to trigger power generation
generate_button = tk.Button(root, text="Generate Power", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", command=update_gui, relief="raised", width=20)
generate_button.pack(pady=15)

# Button to open the website of the power
open_button = tk.Button(root, text="Open Website", font=("Helvetica", 12, "bold"), bg="#2196F3", fg="white", relief="raised", width=20)
open_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
