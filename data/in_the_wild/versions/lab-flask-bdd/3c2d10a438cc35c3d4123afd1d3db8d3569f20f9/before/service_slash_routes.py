######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Pet Store Service with UI

Paths:
------
GET / - Displays a UI for Selenium testing
GET /pets - Returns a list all of the Pets
GET /pets/{id} - Returns the Pet with a given id number
POST /pets - creates a new Pet record in the database
PUT /pets/{id} - updates a Pet record in the database
DELETE /pets/{id} - deletes a Pet record in the database
"""

import sys
import logging
from flask import jsonify, request, json, url_for, make_response, abort
from . import app
from service.models import Pet
from .utils import status  # HTTP Status Codes
from .utils import error_handlers


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/healthcheck")
def healthcheck():
    """Let them know our heart is still beating"""
    return make_response(jsonify(status=200, message="Healthy"), status.HTTP_200_OK)


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    # data = '{name: <string>, category: <string>}'
    # url = request.base_url + 'pets' # url_for('list_pets')
    # return jsonify(name='Pet Demo REST API Service', version='1.0', url=url, data=data), status.HTTP_200_OK
    return app.send_static_file("index.html")


######################################################################
# LIST ALL PETS
######################################################################
@app.route("/pets", methods=["GET"])
def list_pets():
    """Returns all of the Pets"""
    app.logger.info("Request to list Pets...")

    pets = []
    category = request.args.get("category")
    name = request.args.get("name")
    available = request.args.get("available")

    if available:  # convert to boolean
        available = available.lower() in ["true", "yes", "1"]
    if category:
        app.logger.info("Find by category: %s", category)
        pets = Pet.find_by_category(category)
    elif name:
        app.logger.info("Find by name: %s", name)
        pets = Pet.find_by_name(name)
    elif available:
        app.logger.info("Find by available: %s", available)
        pets = Pet.find_by_availability(available)
    else:
        app.logger.info("Find all")
        pets = Pet.all()

    app.logger.info("[%s] Pets returned", len(pets))
    results = [pet.serialize() for pet in pets]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# RETRIEVE A PET
######################################################################
@app.route("/pets/<pet_id>", methods=["GET"])
def get_pets(pet_id):
    """
    Retrieve a single Pet

    This endpoint will return a Pet based on it's id
    """
    app.logger.info("Request to Retrieve a pet with id [%s]", pet_id)

    pet = Pet.find(pet_id)
    if not pet:
        abort(status.HTTP_404_NOT_FOUND, f"Pet with id '{pet_id}' was not found.")

    app.logger.info("Returning pet: %s", pet.name)
    return make_response(jsonify(pet.serialize()), status.HTTP_200_OK)


######################################################################
# CREATE A NEW PET
######################################################################
@app.route("/pets", methods=["POST"])
def create_pets():
    """
    Creates a Pet
    This endpoint will create a Pet based the data in the body that is posted
    """
    app.logger.info("Request to Create a Pet...")
    data = {}
    # Check for form submission data
    if request.headers.get("Content-Type") == "application/x-www-form-urlencoded":
        app.logger.info("Getting data from form submit")
        data = {"name": request.form["name"], "category": request.form["category"], "available": True, "gender": "UNKNOWN"}
    else:
        check_content_type("application/json")
        app.logger.info("Getting json data from API call")
        data = request.get_json()

    app.logger.info(data)
    pet = Pet()
    pet.deserialize(data)
    pet.create()
    app.logger.info("Pet with new id [%s] saved!", pet.id)

    message = pet.serialize()
    location_url = url_for("get_pets", pet_id=pet.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED, {"Location": location_url})


######################################################################
# UPDATE AN EXISTING PET
######################################################################
@app.route("/pets/<pet_id>", methods=["PUT"])
def update_pets(pet_id):
    """
    Update a Pet

    This endpoint will update a Pet based the body that is posted
    """
    app.logger.info("Request to Update a pet with id [%s]", pet_id)
    check_content_type("application/json")

    pet = Pet.find(pet_id)
    if not pet:
        abort(status.HTTP_404_NOT_FOUND, f"Pet with id '{pet_id}' was not found.")

    data = request.get_json()
    app.logger.info(data)
    pet.deserialize(data)
    pet.id = pet_id
    pet.update()
    return make_response(jsonify(pet.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A PET
######################################################################
@app.route("/pets/<pet_id>", methods=["DELETE"])
def delete_pets(pet_id):
    """
    Delete a Pet

    This endpoint will delete a Pet based the id specified in the path
    """
    app.logger.info("Request to Delete a pet with id [%s]", pet_id)

    pet = Pet.find(pet_id)
    if pet:
        pet.delete()

    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
# PURCHASE A PET
######################################################################
@app.route("/pets/<pet_id>/purchase", methods=["PUT"])
def purchase_pets(pet_id):
    """Purchasing a Pet makes it unavailable"""
    pet = Pet.find(pet_id)
    if not pet:
        abort(status.HTTP_404_NOT_FOUND, "Pet with id '{}' was not found.".format(pet_id))
    if not pet.available:
        abort(
            status.HTTP_400_BAD_REQUEST,
            "Pet with id '{}' is not available.".format(pet_id),
        )
    pet.available = False
    pet.update()
    return make_response(jsonify(pet.serialize()), status.HTTP_200_OK)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


@app.before_first_request
def init_db(dbname="pets"):
    """Initlaize the model"""
    Pet.init_db(dbname)


# load sample data
def data_load(payload):
    """Loads a Pet into the database"""
    pet = Pet(payload["name"], payload["category"], payload["available"])
    pet.create()


def data_reset():
    """Removes all Pets from the database"""
    if app.testing:
        Pet.remove_all()


def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            "Content-Type must be {}".format(content_type),
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(content_type),
    )


# @app.before_first_request
def initialize_logging(log_level=app.config["LOGGING_LEVEL"]):
    """Initialized the default logging to STDOUT"""
    if not app.debug:
        print("Setting up logging...")
        # Set up default logging for submodules to use STDOUT
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)
        # Remove the Flask default handlers and use our own
        handler_list = list(app.logger.handlers)
        for log_handler in handler_list:
            app.logger.removeHandler(log_handler)
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        app.logger.info("Logging handler established")
