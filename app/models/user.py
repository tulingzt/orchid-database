from app import db
from marshmallow import Schema, fields, validate

# 用户信息模型定义
class User(db.Model):
    # 表名定义
    __tablename__ = 'user'
    # 表项定义
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户唯一ID')
    username = db.Column(db.String(50), unique=True, nullable=False, comment='用户名（唯一）')
    password_hash = db.Column( db.String(255), nullable=False, comment='密码哈希值')
    role = db.Column( db.Enum('admin', 'user', name='user_role'), nullable=False, default='user', comment='用户权限')
    created_time = db.Column( db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'), comment='注册时间')
    last_login_time = db.Column( db.TIMESTAMP, nullable=True, comment='最后登录时间')
    # 提供转字典方法
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "role": self.role,
            "created_time": self.created_time,
            "last_login_time": self.last_login_time
        }
    # 更新登录时间
    def update_login_time(self):
        self.last_login_time = db.text('CURRENT_TIMESTAMP')
        db.session.add(self)
        db.session.commit()
    # 表属性定义
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci',
        'comment': '用户信息表'
    }

# 用户查询数据校验
class UserQuerySchema(Schema):
    username = fields.Str(required=False, allow_none=True)
    role = fields.Str(required=False, allow_none=True, validate=validate.OneOf(['admin', 'user']))
    page = fields.Int(required=False, missing=1, validate=validate.Range(min=1))
    limit = fields.Int(required=False, missing=10, validate=validate.Range(min=1, max=100))
