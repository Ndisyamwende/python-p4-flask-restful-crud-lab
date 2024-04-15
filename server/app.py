#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):

    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)


api.add_resource(Plants, '/plants')


class PlantByID(Resource):

    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(plant), 200)


api.add_resource(PlantByID, '/plants/<int:id>')

class UpdatePlant(Resource):

    def patch(self, id):
        # Fetch the plant from the database
        plant = Plant.query.get_or_404(id)

        # Get the data from the request body
        data = request.json

        # Update the plant attributes
        if 'is_in_stock' in data:
            plant.is_in_stock = data['is_in_stock']

        # Commit the changes to the database
        db.session.commit()

        # Return the updated plant as JSON
        return make_response(plant.to_dict(), 200)


api.add_resource(UpdatePlant, '/plants/<int:id>')

class DeletePlant(Resource):

    def delete(self, id):
        # Fetch the plant from the database
        plant = Plant.query.get_or_404(id)

        # Delete the plant
        db.session.delete(plant)
        db.session.commit()

        # Return no content
        return make_response('', 204)


api.add_resource(DeletePlant, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
