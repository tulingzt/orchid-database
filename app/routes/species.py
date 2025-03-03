from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.models.orchid_species import Species, SpeciesSchema
from app import db

species = Blueprint('species', __name__)

# 兰花种类表路由
# 添加新种类（管理员）
@species.route('/species', methods=['POST'])
@jwt_required()
def add_species():
    if get_jwt()['role'] != 'admin':
        return jsonify({"code": 403, "message": "权限不足"}), 403
    data = SpeciesSchema().load(request.json)
    new_species = Species(**data)
    db.session.add(new_species)
    db.session.commit()
    return jsonify({"code": 201, "data": {"species_id": new_species.species_id}}), 201

# 更新种类信息（管理员）
@species.route('/species/<int:species_id>', methods=['PUT'])
@jwt_required()
def update_species(species_id):
    if get_jwt()['role'] != 'admin':
        return jsonify({"code": 403, "message": "权限不足"}), 403
    data = SpeciesSchema().load(request.json)
    species = Species.query.get_or_404(species_id)
    for key, value in data.items():
        setattr(species, key, value)
    db.session.commit()
    return jsonify({"code": 200, "data": species.to_dict()}), 200

# 删除种类（级联删除关联数据，管理员）
@species.route('/species/<int:species_id>', methods=['DELETE'])
@jwt_required()
def delete_species(species_id):
    if get_jwt()['role'] != 'admin':
        return jsonify({"code": 403, "message": "权限不足"}), 403
    species = Species.query.get_or_404(species_id)
    db.session.delete(species)
    db.session.commit()
    return jsonify({"code": 204, "message": "物种删除成功"}), 204

# 查询种类信息
@species.route('/species/<int:species_id>', methods=['GET'])
def get_species(species_id):
    species = Species.query.get_or_404(species_id)
    return jsonify({"code": 200, "data": species.to_dict()}), 200

# 查询多条种类信息（分页+过滤）
@species.route('/species', methods=['GET'])
def get_multiple_species():
    query = Species.query
    # 基础查询：按科、属、保护级别过滤
    if family := request.args.get('family'):
        query = query.filter_by(family=family)
    if genus := request.args.get('genus'):
        query = query.filter_by(genus=genus)
    if conservation_status := request.args.get('conservation_status'):
        query = query.filter_by(conservation_status=conservation_status)
    # 模糊查询：按学名、中文名过滤
    if scientific_name := request.args.get('scientific_name'):
        query = query.filter(Species.scientific_name.like(f"%{scientific_name}%"))
    if chinese_name := request.args.get('chinese_name'):
        query = query.filter(Species.chinese_name.like(f"%{chinese_name}%"))
    # 分页查询
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return jsonify({
        "code": 200,
        "data": [specie.to_dict() for specie in pagination.items],
        "pagination": {
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
            "per_page": pagination.per_page
        }
    })