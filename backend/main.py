from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask import request

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # This keeps the warning messages away
db_uri = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@"+db_uri+"/postgres"

db = SQLAlchemy(app)
db.init_app(app)

class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120), nullable=False)

    def __init__(self, text):
        self.text = text
    
    def __repr__(self):
        return f"<Text {self.text}>"

@app.route('/fetch')
def fetch():
    words = Text.query.all()
    results = [
        {
            "text": word.text
        } for word in words]
    return {"texts": results}, 200

@app.route('/add', methods=['POST'])
def add():
    text = request.json['text']
    db.session.add(Text(text=text))
    db.session.commit()
    return 'Done', 201

@app.route('/delete', methods=['DELETE'])
def delete():
    db.session.query(Text).delete()
    db.session.commit()
    return 'Done', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0')
