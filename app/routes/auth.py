from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import bcrypt
from app.models.user import User
from app import db

# 用户认证路由
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # 校验唯一性
    if User.query.filter_by(username=username).first():
        return jsonify({"code": 400, "message": "用户名已存在"}), 400
    # 哈希密码
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    # 保存用户
    new_user = User(username, password_hash=password_hash.decode('utf-8'), role='user')
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"code": 201, "message": "注册成功"}), 201
        
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # 查找是否有对应用户
    user = User.query.filter_by(username = username).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return jsonify({"code": 401, "message": "用户名或密码错误"}), 401
    # 生成JWT令牌
    user.update_login_time()
    access_token = create_access_token(identity = user.user_id, additional_claims = {"role": user.role})
    refresh_token = create_refresh_token(identity = user.user_id, additional_claims = {"role": user.role})
    return jsonify(access_token = access_token, refresh_token = refresh_token)

# 使用刷新JWT来获取普通JWT
@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh = True)
def refresh():
    user_id = get_jwt_identity()
    role = get_jwt_identity()["role"]
    access_token = create_access_token(identity = user_id, additional_claims = {"role": role})
    return jsonify(access_token = access_token)
    
from flask_jwt_extended import jwt_required, get_jwt_identity
@auth.route('/protected', methods=["GET"])
@jwt_required()  # 需要身份验证才能访问
def protected_route():
    current_user_id = get_jwt_identity()
    current_user_name = get_jwt_identity()["username"]
    return jsonify(id = current_user_id, name = current_user_name), 200