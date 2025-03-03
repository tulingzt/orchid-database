from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.models.flower_morphology import Flower
from app.models.petal_morphology import Petal, PetalSchema
from app import db

petal = Blueprint('petal', __name__)

# 花瓣形态表路由
# 添加新花瓣（管理员）
@petal.route('/petal', methods=['POST'])
@jwt_required()
def add_petal():
    if get_jwt()['role'] != 'admin':
        return jsonify({"code": 403, "message": "权限不足"}), 403
    data = PetalSchema().load(request.json)
    new_petal = Petal(**data)
    db.session.add(new_petal)
    db.session.commit()
    return jsonify({"code": 201, "data": {"petal_id": new_petal.petal_id}}), 201

# 更新花瓣信息（管理员）
@petal.route('/petal/<int:petal_id>', methods=['PUT'])
@jwt_required()
def update_petal(petal_id):
    if get_jwt()['role'] != 'admin':
        return jsonify({"code": 403, "message": "权限不足"}), 403
    data = PetalSchema().load(request.json)
    petal = Petal.query.get_or_404(petal_id)
    for key, value in data.items():
        setattr(petal, key, value)
    db.session.commit()
    return jsonify({"code": 200, "data": petal.to_dict()}), 200

# 删除花瓣信息（管理员）
@petal.route('/petal/<int:petal_id>', methods=['DELETE'])
@jwt_required()
def delete_petal(petal_id):
    if get_jwt()['role'] != 'admin':
        return jsonify({"code": 403, "message": "权限不足"}), 403
    petal = Petal.query.get_or_404(petal_id)
    db.session.delete(petal)
    db.session.commit()
    return jsonify({"code": 204, "message": "花瓣数据删除成功"}), 204

# 查询花瓣信息
@petal.route('/petal/<int:petal_id>', methods=['GET'])
def get_petal(petal_id):
    petal = Petal.query.get_or_404(petal_id)
    return jsonify({"code": 200, "data": petal.to_dict()}), 200

# 查询多条花瓣信息（分页+过滤）
@petal.route('/petal', methods=['GET'])
def get_multiple_petal():
    # 初始化联合查询
    query = Petal.query.join(
        Flower, 
        Flower.flower_id == Petal.flower_id
    )
    # 基础查询：按种类过滤
    if species_ids := request.args.get('species_ids'):
        ids_list = list(map(int, species_ids.split(',')))
        query = query.filter(Flower.species_id.in_(ids_list))
    # 高级查询：按尺寸范围过滤
    if min_length := request.args.get('min_length', type=float):
        query = query.filter(Petal.petal_length >= min_length)
    if max_length := request.args.get('max_length', type=float):
        query = query.filter(Petal.petal_length <= max_length)
    if min_width := request.args.get('min_width', type=float):
        query = query.filter(Petal.petal_width >= min_width)
    if max_width := request.args.get('max_width', type=float):
        query = query.filter(Petal.petal_width <= max_width)
    if min_area := request.args.get('min_area', type=float):
        query = query.filter(Petal.petal_area >= min_area)
    if max_area := request.args.get('max_area', type=float):
        query = query.filter(Petal.petal_area <= max_area)
    # 分页查询
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return jsonify({
        "code": 200,
        "data": [petal.to_dict() for petal in pagination.items],
        "pagination": {
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
            "per_page": pagination.per_page
        }
    })
