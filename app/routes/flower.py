from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.models.flower_morphology import Flower, FlowerSchema
from app import db

flower = Blueprint('flower', __name__)

# 花朵形态表路由
# 添加新花朵（管理员）
@flower.route('/flower', methods=['POST'])
@jwt_required()
def add_flower():
    if get_jwt()['role'] != 'admin':
        return jsonify({"code": 403, "message": "权限不足"}), 403
    data = FlowerSchema().load(request.json)
    new_flower = Flower(**data)
    db.session.add(new_flower)
    db.session.commit()
    return jsonify({"code": 201, "data": {"flower_id": new_flower.flower_id}}), 201

# 更新花朵信息（管理员）
@flower.route('/flower/<int:flower_id>', methods=['PUT'])
@jwt_required()
def update_flower(flower_id):
    if get_jwt()['role'] != 'admin':
        return jsonify({"code": 403, "message": "权限不足"}), 403
    data = FlowerSchema().load(request.json)
    flower = Flower.query.get_or_404(flower_id)
    for key, value in data.items():
        setattr(flower, key, value)
    db.session.commit()
    return jsonify({"code": 200, "data": flower.to_dict()}), 200

# 删除花朵信息（级联删除关联数据，管理员）
@flower.route('/flower/<int:flower_id>', methods=['DELETE'])
@jwt_required()
def delete_flower(flower_id):
    if get_jwt()['role'] != 'admin':
        return jsonify({"code": 403, "message": "权限不足"}), 403
    flower = Flower.query.get_or_404(flower_id)
    db.session.delete(flower)
    db.session.commit()
    return jsonify({"code": 204, "message": "花朵数据删除成功"}), 204

# 查询花朵信息
@flower.route('/flower/<int:flower_id>', methods=['GET'])
def get_flower(flower_id):
    flower = Flower.query.get_or_404(flower_id)
    return jsonify({"code": 200, "data": flower.to_dict()}), 200

# 查询多条花朵信息（分页+过滤）
@flower.route('/flower', methods=['GET'])
def get_multiple_flower():
    query = Flower.query
    # 基础查询：按种类过滤
    if species_ids := request.args.get('species_ids'):
        ids_list = list(map(int, species_ids.split(',')))
        query = query.filter(Flower.species_id.in_(ids_list))
    # 高级查询：按尺寸范围过滤
    if min_length := request.args.get('min_length', type=float):
        query = query.filter(Flower.flower_length >= min_length)
    if max_length := request.args.get('max_length', type=float):
        query = query.filter(Flower.flower_length <= max_length)
    if min_width := request.args.get('min_width', type=float):
        query = query.filter(Flower.flower_width >= min_width)
    if max_width := request.args.get('max_width', type=float):
        query = query.filter(Flower.flower_width <= max_width)
    if min_area := request.args.get('min_area', type=float):
        query = query.filter(Flower.flower_area >= min_area)
    if max_area := request.args.get('max_area', type=float):
        query = query.filter(Flower.flower_area <= max_area)
    # 分页查询
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return jsonify({
        "code": 200,
        "data": [flower.to_dict() for flower in pagination.items],
        "pagination": {
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
            "per_page": pagination.per_page
        }
    })