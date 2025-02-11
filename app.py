from flask import Flask, render_template, redirect, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Global variables
power_history = []  # Keep history of the last 10 powers
current_url = ""  # To store the URL of the current power

# Function to retrieve the random power and capabilities
def get_random_power():
    try:
        url = "https://powerlisting.fandom.com/wiki/Special:Random"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract the power name using the span class "mw-page-title-main"
        power_name = soup.find('span', {'class': 'mw-page-title-main'}).get_text(strip=True)

        # Check if the power name contains "Fanon:"
        if "Fanon:" in power_name:
            return get_random_power()  # Reroll if the power name contains "Fanon:"

        if "Trait:" in power_name:
            return get_random_power()  # Reroll if the power name contains "Trait:"

        # Extract capabilities
        capabilities = "Capabilities not available"
        capabilities_section = soup.find('span', {'id': 'Capabilities'})
        
        if capabilities_section:
            capabilities_paragraph = capabilities_section.find_next('p')
            if capabilities_paragraph:
                capabilities = capabilities_paragraph.get_text(strip=True)
        
        power_url = response.url  # Current power URL
        return power_name, capabilities, power_url

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error", f"An error occurred: {e}", ""


# Home route - Display random power and the last 10 powers
@app.route('/')
def home():
    power, capabilities, url = get_random_power()

    # Add the current power to history (keep last 10 powers)
    power_history.insert(0, (power, capabilities, url))
    if len(power_history) > 10:
        power_history.pop()

    return render_template('index.html', power=power, capabilities=capabilities, url=url, power_history=power_history, enumerate=enumerate)


# Route to show details of a specific power from history
@app.route('/power/<int:power_index>')
def show_power(power_index):
    power, capabilities, url = power_history[power_index]
    return render_template('index.html', power=power, capabilities=capabilities, url=url, power_history=power_history, enumerate=enumerate)


# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

