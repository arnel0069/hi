from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/destinations')
def destinations():
    return render_template('destinations.html')

@app.route('/culture')
def culture():
    return render_template('culture.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Process the data (e.g., send an email or store it in a database)
        # For simplicity, let's just print the data in the console
        print(f"Received message from {name} ({email}): {message}")

        # Optionally, send a confirmation or success message
        return redirect(url_for('thank_you'))  # Redirect to a thank you page

    return render_template('contact_us.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
