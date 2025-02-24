from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
import bcrypt
from app.models.user import User
from app import db
import config

# 用户认证路由
auth = Blueprint('auth', __name__)

# 用户注册
@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    admin_secret = data.get('admin_secret')
    # 校验唯一性
    if User.query.filter_by(username=username).first():
        return jsonify({"code": 400, "message": "用户名已存在"}), 400
    # 哈希密码
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    # 判断是否为管理员注册
    role = 'user'
    if admin_secret and admin_secret == config.auth.ADMIN_SECRET:
        role = 'admin'
    # 保存用户
    new_user = User(username, password_hash = password_hash.decode('utf-8'), role = role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"code": 201, "message": "注册成功"}), 201

# 用户登录
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # 查找是否有对应用户
    user = User.query.filter_by(username = username).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return jsonify({"code": 401, "message": "用户名或密码错误"}), 401
    user.update_login_time()
    # 生成JWT令牌
    access_token = create_access_token(identity = user.username, additional_claims = {"id": user.user_id, "name": user.username, "role": user.role})
    refresh_token = create_access_token(identity = user.username, additional_claims = {"id": user.user_id, "name": user.username, "role": user.role})
    return jsonify(access_token = access_token, refresh_token = refresh_token)

@auth.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user = get_jwt()
    if current_user['role'] != 'admin':
        return jsonify({"code": 403, "message": "权限不足"}), 403
    users = User.query.all()
    return jsonify([{
        "user_id": u.user_id,
        "username": u.username,
        "role": u.role
    } for u in users])

# 管理员修改用户权限
@auth.route('/role/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user_role(user_id):
    # 获取权限
    current_user = get_jwt()
    if current_user['role'] != 'admin':
        return jsonify({"code": 403, "message": "权限不足"}), 403
    new_role = request.json.get('role')
    # 寻找修改对象
    user = User.query.get(user_id)
    if not user:
        return jsonify({"code": 404, "message": "用户不存在"}), 404
    # 更新
    user.role = new_role
    db.session.commit()
    return jsonify({"code": 200, "message": "角色更新成功"})

# 使用刷新JWT来获取普通JWT
@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh = True)
def refresh():
    current_user = get_jwt()
    access_token = create_access_token(identity = current_user['name'], additional_claims = {"id": current_user['id'], "name": current_user['name'], "role": current_user['role']})
    return jsonify(access_token = access_token)