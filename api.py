from flask import Flask, request, make_response, g, jsonify
from http import HTTPStatus
import pydantic

from storage.db_connect import get_session
from storage.db_io import (
    store_animal,
    retrieve_animal,
    retrieve_animals_by_genus,
    generator_retrieve_plant_by_genus,
)
from utils.models import Animal
from utils.streaming import format_streaming_response


app = Flask(__name__)


@app.before_request
def get_db_session():
    g.session = get_session()


@app.route('/animal/<genus>/<species>')
def get_animal(genus, species):
    animal = retrieve_animal(g.session, genus, species)
    if animal:
        return jsonify(animal.dict())
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return animal


@app.route('/animal/<genus>')
def get_animals(genus):
    animals = retrieve_animals_by_genus(g.session, genus)
    return jsonify([animal.dict() for animal in animals])


@app.route('/animal', methods=['POST'])
def post_animal():
    try:
        animal = Animal(**request.get_json())
    except pydantic.error_wrappers.ValidationError as e:
        response = make_response(str(e), HTTPStatus.UNPROCESSABLE_ENTITY)
        return response
    store_animal(g.session, animal)
    return {"inserted": True}


@app.route('/plant/<genus>')
def get_plant(genus):
    plants = generator_retrieve_plant_by_genus(g.session, genus)
    return format_streaming_response(plants), {"Content-Type": "application/json"}
