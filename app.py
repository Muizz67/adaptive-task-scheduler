from flask import Flask, render_template
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/')
def schedule():
    # Here you can add any logic to fetch or prepare data for your schedule
    # For now, we'll just render the template
    return render_template('schedule.html')

if __name__ == '__main__':
    app.run(debug=True)
