from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')  # Use SQLite for development
db = SQLAlchemy(app)

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
        
        # Create a new Message record in the database
        new_message = Message(name=name, email=email, message=message)
        
        try:
            # Add and commit the transaction to the database
            db.session.add(new_message)
            db.session.commit()
            print(f"Message from {name} ({email}) stored successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error storing message: {e}")
            return render_template('contact_us.html', error="There was an error processing your request.")
        
        # Redirect to a thank you page
        return redirect(url_for('thank_you'))

    return render_template('contact_us.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

# Define the Message model to store form data
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Message {self.id}, {self.name}, {self.email}>'

# Create the database tables (if they don't exist yet)
with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Default to port 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port)
