from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Impor CORS

app = Flask(__name__)
CORS(app, resources={r"/tickets/*": {"origins": "http://localhost:3000"}})  # Menambahkan CORS ke aplikasi Flask

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'date': self.date
        }

@app.route('/tickets', methods=['GET'])
def get_tickets():
    tickets = Ticket.query.all()
    return jsonify([ticket.to_dict() for ticket in tickets])

@app.route('/tickets', methods=['POST'])
def create_ticket():
    data = request.get_json()
    new_ticket = Ticket(name=data['name'], price=data['price'], date=data['date'])
    db.session.add(new_ticket)
    db.session.commit()
    return jsonify(new_ticket.to_dict()), 201

@app.route('/tickets/<int:id>', methods=['DELETE'])
def delete_ticket(id):
    ticket = Ticket.query.get(id)
    if not ticket:
        return jsonify({'error': 'Ticket not found'}), 404
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({'message': 'Ticket deleted'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
