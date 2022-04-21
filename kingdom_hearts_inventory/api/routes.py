from flask import Blueprint, request, jsonify
from kingdom_hearts_inventory.helpers import token_required
from kingdom_hearts_inventory.models import db, User, Character, character_schema, characters_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required 
def getdata(current_user_token):
    return { 'some': 'value'}

# create Character endpoint
@api.route('/characters', methods = ['POST'])
@token_required
def create_character(current_user_token):
    name = request.json['name']
    homeworld = request.json['homeworld']
    weapon = request.json['weapon']
    species = request.json['species']
    gender = request.json['gender']
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token.token}")

    character = Character(name, homeworld, weapon, species, gender, user_token = user_token)

    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)

# retrieve all Character endpoint
@api.route('/characters', methods = ['GET'])
@token_required
def get_characters(current_user_token):
    owner = current_user_token.token
    characters = Character.query.filter_by(user_token = owner).all()
    response = characters_schema.dump(characters)
    return jsonify(response)

# retrieve one Character endpoint
@api.route('/characters/<id>', methods = ['GET'])
@token_required
def get_character(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        character = Character.query.get(id)
        response = character_schema.dump(character)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401

# update Character endpoint
@api.route('/characters/<id>', methods = ['POST', 'PUT'])
@token_required
def update_character(current_user_token, id):
    character = Character.query.get(id) # grab character instance

    character.name = request.json['name']   
    character.homeworld = request.json['homeworld']
    character.weapon = request.json['weapon']
    character.species = request.json['species']
    character.gender = request.json['gender']
    character.user_token = current_user_token.token

    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)

# delete Character endpoint
@api.route('/characters/<id>', methods = ['DELETE'])
@token_required
def delete_character(current_user_token, id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)