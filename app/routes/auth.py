from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt
import bcrypt
from app.models.user import User, UserQuerySchema
from app import db
import config

# 用户认证路由
auth = Blueprint('auth', __name__)

# 用户注册
@auth.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    # 校验唯一性
    if User.query.filter_by(username = username).first():
        return jsonify({"code": 400, "message": "用户名已存在"}), 400
    # 哈希密码
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    # 判断是否为管理员注册
    role = 'user'
    if request.json.get('admin_secret') == config.auth.ADMIN_SECRET:
        role = 'admin'
    # 保存用户
    new_user = User(username, password_hash = password_hash.decode('utf-8'), role = role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"code": 201, "message": "注册成功"}), 201

# 用户登录
@auth.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    # 查找是否有对应用户
    user = User.query.filter_by(username = username).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return jsonify({"code": 401, "message": "用户名或密码错误"}), 401
    user.update_login_time()
    # 生成JWT令牌
    access_token = create_access_token(
        identity=user.username,
        additional_claims = {
            "id": user.user_id,
            "name": user.username,
            "role": user.role
        }
    )
    refresh_token = create_refresh_token(
        identity=user.username,
        additional_claims = {
            "id": user.user_id,
            "name": user.username,
            "role": user.role
        }
    )
    return jsonify(access_token=access_token, refresh_token=refresh_token)

# 管理员修改用户权限
@auth.route('/role/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user_role(user_id):
    if get_jwt()['role'] != 'admin':
        return jsonify({"code": 403, "message": "权限不足"}), 403
    new_role = request.json.get('role')
    user = User.query.get_or_404(user_id)
    user.role = new_role
    db.session.commit()
    return jsonify({"code": 200, "message": "用户权限更新成功"})

# 删除用户
@auth.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    if get_jwt()['role'] != 'admin':
        return jsonify({"code": 403, "message": "权限不足"}), 403
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"code": 204, "message": "用户删除成功"})

# 查询用户 支持模糊查询
@auth.route('/users', methods=['GET'])
@jwt_required()
def get_user():
    if get_jwt()['role'] != 'admin':
        return jsonify({"code": 403, "message": "权限不足"}), 403
    # 校验查询参数
    UserQuerySchema().load(request.args)
    query = User.query
    # 模糊匹配用户名
    if username := request.args.get('username'):
        query = query.filter(User.username.like(f"%{username}%"))
    # 权限仍为精确匹配
    if role := request.args.get('role'):
        query = query.filter_by(role=role)
    # 分页查询
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    return jsonify({
        "code": 200,
        "data": [user.to_dict() for user in pagination.items],
        "pagination": {
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
            "per_page": pagination.per_page
        }
    })

# 使用刷新JWT来获取普通JWT
@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh = True)
def refresh():
    current_user = get_jwt()
    access_token = create_access_token(
        identity=current_user['name'],
        additional_claims = {
            "id": current_user['id'],
            "name": current_user['name'],
            "role": current_user['role']
        }
    )
    return jsonify(access_token=access_token)