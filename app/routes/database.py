from flask import Blueprint
from app.models.orchid_species import OrchidSpecies
from app.models.flower_morphology import FlowerMorphology
from app.models.petal_morphology import PetalMorphology
from app.models.sepal_morphology import SepalMorphology
from app import db

# 兰花种类表路由
orchid_species = Blueprint('orchid_species', __name__)

@orchid_species.route('/add')
def add():
    new_species = OrchidSpecies('兰科', '兰属', 'Cymbidium ensifolium', '建兰', '安徽、浙江、江西、湖南、湖北、四川、贵州、云南、西藏、福建、台湾、广东、广西、海南', '易危')
    db.session.add(new_species)
    new_species = OrchidSpecies('兰科', '兰属', 'Cymbidium goeringii', '春兰', '河南、陕西、甘肃、安徽、江苏、浙江、江西、湖南、湖北、四川、贵州、云南、福建、台湾、广东、广西', '易危')
    db.session.add(new_species)
    db.session.commit()
    return 'species added!'

@orchid_species.route('/get')
def get():
    species = OrchidSpecies.query.all()
    return '<br>'.join([f'{specie.family} {specie.genus} {specie.scientific_name} {specie.distribution} {specie.conservation_status}' for specie in species])

@orchid_species.route("/")
def hello():
    return "Hello orchid species!"

# 花朵形态表路由
flower_morphology = Blueprint('flower_morphology', __name__)

@flower_morphology.route('/add')
def add():
    new_flower = FlowerMorphology(1, 1.5, 2.5, 5.0)
    db.session.add(new_flower)
    new_flower = FlowerMorphology(1, 2.5, 2.5, 5.0)
    db.session.add(new_flower)
    new_flower = FlowerMorphology(2, 1.5, 2.5, 5.0)
    db.session.add(new_flower)
    new_flower = FlowerMorphology(2, 1.5, 3.5, 5.0)
    db.session.add(new_flower)
    db.session.commit()
    return 'species added!'

@flower_morphology.route('/get')
def get():
    flowers = FlowerMorphology.query.all()
    return '<br>'.join([f'{flower.flower_id} {flower.species_id} {flower.flower_length} {flower.flower_width} {flower.flower_ratio} {flower.flower_area}' for flower in flowers])

@flower_morphology.route("/")
def hello():
    return "Hello flower morphology!"

# 花瓣形态表路由
petal_morphology = Blueprint('petal_morphology', __name__)

@petal_morphology.route('/add')
def add():
    new_petal = PetalMorphology(1, 1.5, 2.5, 5.0)
    db.session.add(new_petal)
    new_petal = PetalMorphology(1, 2.5, 2.5, 5.0)
    db.session.add(new_petal)
    new_petal = PetalMorphology(2, 1.5, 2.5, 5.0)
    db.session.add(new_petal)
    new_petal = PetalMorphology(2, 1.5, 3.5, 5.0)
    db.session.add(new_petal)
    db.session.commit()
    return 'new_petal added!'

@petal_morphology.route('/get')
def get():
    petals = PetalMorphology.query.all()
    return '<br>'.join([f'{petal.petal_id} {petal.flower_id} {petal.petal_length} {petal.petal_width} {petal.petal_ratio} {petal.petal_area}' for petal in petals])

@petal_morphology.route("/")
def hello():
    return "Hello petal morphology!"

# 萼片形态表路由
sepal_morphology = Blueprint('sepal_morphology', __name__)

@sepal_morphology.route('/add')
def add():
    new_sepal = SepalMorphology(1, 1.5, 2.5, 5.0)
    db.session.add(new_sepal)
    new_sepal = SepalMorphology(1, 2.5, 2.5, 5.0)
    db.session.add(new_sepal)
    new_sepal = SepalMorphology(2, 1.5, 2.5, 5.0)
    db.session.add(new_sepal)
    new_sepal = SepalMorphology(2, 1.5, 3.5, 5.0)
    db.session.add(new_sepal)
    db.session.commit()
    return 'new_sepal added!'

@sepal_morphology.route('/get')
def get():
    sepals = SepalMorphology.query.all()
    return '<br>'.join([f'{sepal.sepal_id} {sepal.flower_id} {sepal.sepal_length} {sepal.sepal_width} {sepal.sepal_ratio} {sepal.sepal_area}' for sepal in sepals])

@sepal_morphology.route("/")
def hello():
    return "Hello sepal morphology!"