from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    # 注册蓝图
    from app.routes.database import orchid_species
    app.register_blueprint(orchid_species, url_prefix='/orchid-species')
    from app.routes.database import flower_morphology
    app.register_blueprint(flower_morphology, url_prefix='/flower-morphology')
    from app.routes.database import petal_morphology
    app.register_blueprint(petal_morphology, url_prefix='/petal-morphology')
    from app.routes.database import sepal_morphology
    app.register_blueprint(sepal_morphology, url_prefix='/sepal-morphology')
    # 初始化数据库配置
    db.init_app(app)
    # 创建所有未存在的数据库
    with app.app_context():
        db.create_all()
    return app