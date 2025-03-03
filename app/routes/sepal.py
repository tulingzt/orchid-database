from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.models.flower_morphology import Flower
from app.models.sepal_morphology import Sepal, SepalSchema
from app import db

sepal = Blueprint('sepal', __name__)

# 萼片形态表路由
# 添加新萼片（管理员）
@sepal.route('/sepal', methods=['POST'])
@jwt_required()
def add_sepal():
    if get_jwt()['role'] != 'admin':
        return jsonify({"code": 403, "message": "权限不足"}), 403
    data = SepalSchema().load(request.json)
    new_sepal = Sepal(**data)
    db.session.add(new_sepal)
    db.session.commit()
    return jsonify({"code": 201, "data": {"sepal_id": new_sepal.sepal_id}}), 201

# 更新萼片信息（管理员）
@sepal.route('/sepal/<int:sepal_id>', methods=['PUT'])
@jwt_required()
def update_sepal(sepal_id):
    if get_jwt()['role'] != 'admin':
        return jsonify({"code": 403, "message": "权限不足"}), 403
    data = SepalSchema().load(request.json)
    sepal = Sepal.query.get_or_404(sepal_id)
    for key, value in data.items():
        setattr(sepal, key, value)
    db.session.commit()
    return jsonify({"code": 200, "data": sepal.to_dict()}), 200

# 删除萼片信息（管理员）
@sepal.route('/sepal/<int:sepal_id>', methods=['DELETE'])
@jwt_required()
def delete_sepal(sepal_id):
    if get_jwt()['role'] != 'admin':
        return jsonify({"code": 403, "message": "权限不足"}), 403
    sepal = Sepal.query.get_or_404(sepal_id)
    db.session.delete(sepal)
    db.session.commit()
    return jsonify({"code": 204, "message": "萼片数据删除成功"}), 204

# 查询萼片信息
@sepal.route('/sepal/<int:sepal_id>', methods=['GET'])
def get_sepal(sepal_id):
    sepal = Sepal.query.get_or_404(sepal_id)
    return jsonify({"code": 200, "data": sepal.to_dict()}), 200

# 查询多条萼片信息（分页+过滤）
@sepal.route('/sepal', methods=['GET'])
def get_multiple_speal():
    # 初始化联合查询
    query = Sepal.query.join(
        Flower, 
        Flower.flower_id == Sepal.flower_id
    )
    # 基础查询：按种类过滤
    if species_ids := request.args.get('species_ids'):
        ids_list = list(map(int, species_ids.split(',')))
        query = query.filter(Flower.species_id.in_(ids_list))
    # 高级查询：按尺寸范围过滤
    if min_length := request.args.get('min_length', type=float):
        query = query.filter(Sepal.sepal_length >= min_length)
    if max_length := request.args.get('max_length', type=float):
        query = query.filter(Sepal.sepal_length <= max_length)
    if min_width := request.args.get('min_width', type=float):
        query = query.filter(Sepal.sepal_width >= min_width)
    if max_width := request.args.get('max_width', type=float):
        query = query.filter(Sepal.sepal_width <= max_width)
    if min_area := request.args.get('min_area', type=float):
        query = query.filter(Sepal.sepal_area >= min_area)
    if max_area := request.args.get('max_area', type=float):
        query = query.filter(Sepal.sepal_area <= max_area)
    # 分页查询
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return jsonify({
        "code": 200,
        "data": [sepal.to_dict() for sepal in pagination.items],
        "pagination": {
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
            "per_page": pagination.per_page
        }
    })