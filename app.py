from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Storage for delays by category
delay_log = {
    "Weather-Related": 0,
    "Supplier Issues": 0,
    "Inventory Shortage": 0,
    "Other": 0
}

# Function to classify delay based on keywords
def classify_delay(description):
    desc = description.lower()
    if "weather" in desc or "snow" in desc or "rain" in desc:
        return "Weather-Related"
    elif "supplier" in desc:
        return "Supplier Issues"
    elif "inventory" in desc or "stock" in desc:
        return "Inventory Shortage"
    else:
        return "Other"

# Home page: Form to submit delays
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        reason = request.form['reason']
        category = classify_delay(reason)
        delay_log[category] += 1
        return redirect(url_for('home'))
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Delay Tracker</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }
            h1 { color: #3333cc; }
            form { margin-bottom: 20px; }
            input[type="text"] { width: 300px; padding: 5px; }
            input[type="submit"], .button {
                padding: 5px 15px;
                background-color: #3333cc;
                color: white;
                border: none;
                margin-right: 10px;
                cursor: pointer;
                text-decoration: none;
            }
            ul { list-style-type: square; }
            li { margin: 5px 0; }
        </style>
    </head>
    <body>
        <h1>Delay Tracker</h1>
        <form method="POST">
            <label>What caused the delay?</label><br><br>
            <input type="text" name="reason" required>
            <input type="submit" value="Log Delay">
        </form>
        <a href="/summary" class="button">View Summary</a>
    </body>
    </html>
    ''')

# Summary page: Shows counts of each category
@app.route('/summary')
def summary():
    sorted_delays = sorted(delay_log.items(), key=lambda x: x[1], reverse=True)
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Delay Summary</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #e6f2ff; padding: 20px; }
            h1 { color: #0066cc; }
            ul { list-style-type: none; padding: 0; }
            li { margin: 10px 0; font-size: 18px; }
            a { 
                display: inline-block; 
                margin-top: 20px; 
                text-decoration: none; 
                color: white; 
                background-color: #0066cc; 
                padding: 10px 20px;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <h1>Summary of Delays</h1>
        <ul>
            {% for category, count in delays %}
                <li><strong>{{ category }}:</strong> {{ count }}</li>
            {% endfor %}
        </ul>
        <a href="/">Back to Log Delays</a>
    </body>
    </html>
    ''', delays=sorted_delays)

# ONLY ADD THIS BOTTOM SECTION DIFFERENTLY FOR ONLINE HOSTING
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))  # Render gives a port automatically
    app.run(host='0.0.0.0', port=port)
