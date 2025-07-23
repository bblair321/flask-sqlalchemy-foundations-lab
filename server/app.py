from flask import Flask, jsonify
from models import db, Earthquake

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake_by_id(id):
    quake = Earthquake.query.get(id)
    if quake:
        return jsonify({
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        }), 200
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    return jsonify({
        "count": len(quakes),
        "quakes": [
            {
                "id": q.id,
                "location": q.location,
                "magnitude": q.magnitude,
                "year": q.year
            } for q in quakes
        ]
    }), 200

if __name__ == "__main__":
    with app.app_context():
        # Create tables if not exist
        db.create_all()

        # Seed data if not already present
        if not Earthquake.query.first():
            quake1 = Earthquake(id=1, location="Chile", magnitude=9.5, year=1960)
            quake2 = Earthquake(id=2, location="Alaska", magnitude=9.2, year=1964)
            db.session.add_all([quake1, quake2])
            db.session.commit()
            print("Seeded earthquake data")

    app.run(port=5555, debug=True)
