from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///birthday_wishes.db'  # SQLite Database
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Folder for song uploads
db = SQLAlchemy(app)

# Database Model for storing birthday details
class BirthdayWish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    song_filename = db.Column(db.String(100), nullable=True)
    unique_link = db.Column(db.String(100), unique=True, nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/create_birthday_wish', methods=['POST'])
def create_birthday_wish():
    data = request.json

    # Handle the song upload
    song = request.files['song']
    song_filename = f"{uuid.uuid4().hex}.mp3"
    song.save(os.path.join(app.config['UPLOAD_FOLDER'], song_filename))

    # Generate a unique link for the birthday wish
    unique_link = uuid.uuid4().hex

    # Save the data to the database
    new_wish = BirthdayWish(
        name=data['name'],
        age=data['age'],
        message=data['message'],
        song_filename=song_filename,
        unique_link=unique_link
    )
    db.session.add(new_wish)
    db.session.commit()

    # Return the unique link for the sender to share
    return jsonify({"link": f"http://127.0.0.1:5000/view_wish/{unique_link}"}), 200

@app.route('/view_wish/<link>', methods=['GET'])
def view_wish(link):
    # Fetch the birthday wish from the database
    wish = BirthdayWish.query.filter_by(unique_link=link).first()
    if not wish:
        return "Wish not found", 404
    
    # Return the wish details (can be an HTML page or JSON)
    return jsonify({
        "name": wish.name,
        "age": wish.age,
        "message": wish.message,
        "song": f"/uploads/{wish.song_filename}"
    })

if __name__ == '__main__':
    app.run(debug=True)
