from app import db
from marshmallow import Schema, fields, validate

# 萼片形态模型定义
class Sepal(db.Model):
    # 表名定义
    __tablename__ = 'sepal_morphology'
    # 表项定义
    sepal_id = db.Column(
        db.INTEGER,
        primary_key = True,
        autoincrement = True,
        comment = '萼片数据ID'
    )
    flower_id = db.Column(
        db.INTEGER,
        db.ForeignKey('flower_morphology.flower_id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable = False,
        comment = '关联花朵ID',
        index = True
    )
    sepal_length = db.Column(
        db.DECIMAL(6, 2),
        nullable = False,
        comment = '萼片长度（cm）'
    )
    sepal_width = db.Column(
        db.DECIMAL(6, 2),
        nullable = False,
        comment = '萼片宽度（cm）'
    )
    sepal_ratio = db.Column(
        db.DECIMAL(6, 2),
        db.Computed('sepal_length / sepal_width'),
        comment = '长宽比（自动计算）'
    )
    sepal_area = db.Column(
        db.DECIMAL(8, 2),
        comment = '萼片面积（cm²）'
    )
    # 提供转字典方法
    def to_dict(self):
        return {
            "sepal_id": self.sepal_id,
            "flower_id": self.flower_id,
            "sepal_length": self.sepal_length,
            "sepal_width": self.sepal_width,
            "sepal_ratio": self.sepal_ratio,
            "sepal_area": self.sepal_area
        }
    # 表属性定义
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci',
        'comment': '萼片形态参数表'
    }

# 萼片形态数据校验
class SepalSchema(Schema):
    flower_id = fields.Int(required=True)
    sepal_length = fields.Decimal(required=True, validate=validate.Range(min=0))
    sepal_width = fields.Decimal(required=True, validate=validate.Range(min=0))
    sepal_area = fields.Decimal(required=False, allow_none=True, validate=validate.Range(min=0))