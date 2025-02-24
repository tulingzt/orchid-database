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
    from app.routes.database import orchid_species
    app.register_blueprint(orchid_species, url_prefix='/api/orchid-species')
    from app.routes.database import flower_morphology
    app.register_blueprint(flower_morphology, url_prefix='/api/flower-morphology')
    from app.routes.database import petal_morphology
    app.register_blueprint(petal_morphology, url_prefix='/api/petal-morphology')
    from app.routes.database import sepal_morphology
    app.register_blueprint(sepal_morphology, url_prefix='/api/sepal-morphology')
    from app.routes.auth import auth
    app.register_blueprint(auth, url_prefix='/api/auth')
    
    from app.routes.main import html
    app.register_blueprint(html)
    # 初始化配置
    db.init_app(app)
    jwt.init_app(app)
    # 创建所有未存在的数据库
    with app.app_context():
        db.create_all()
    return app