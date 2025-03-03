from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

import config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.app')
    # 注册蓝图
    from app.routes.auth import auth
    app.register_blueprint(auth, url_prefix='/api/auth')
    from app.routes.species import species
    app.register_blueprint(species, url_prefix='/api/data')
    from app.routes.flower import flower
    app.register_blueprint(flower, url_prefix='/api/data')
    from app.routes.petal import petal
    app.register_blueprint(petal, url_prefix='/api/data')
    from app.routes.sepal import sepal
    app.register_blueprint(sepal, url_prefix='/api/data')
    
    from app.routes.main import html
    app.register_blueprint(html)
    # 初始化配置
    db.init_app(app)
    jwt.init_app(app)
    # 创建所有未存在的数据库
    with app.app_context():
        db.create_all()
    return app