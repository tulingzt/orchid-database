from app import db
from marshmallow import Schema, fields, validate

# 花瓣形态模型定义
class Petal(db.Model):
    # 表名定义
    __tablename__ = 'petal_morphology'
    # 表项定义
    petal_id = db.Column(
        db.INTEGER,
        primary_key = True,
        autoincrement = True,
        comment = '花瓣数据ID'
    )
    flower_id = db.Column(
        db.INTEGER,
        db.ForeignKey('flower_morphology.flower_id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable = False,
        comment = '关联花朵ID',
        index = True
    )
    petal_length = db.Column(
        db.DECIMAL(6, 2),
        nullable = False,
        comment = '花瓣长度（cm）'
    )
    petal_width = db.Column(
        db.DECIMAL(6, 2),
        nullable = False,
        comment = '花瓣宽度（cm）'
    )
    petal_ratio = db.Column(
        db.DECIMAL(6, 2),
        db.Computed('petal_length / petal_width'),
        comment = '长宽比（自动计算）'
    )
    petal_area = db.Column(
        db.DECIMAL(8, 2),
        comment = '花瓣面积（cm²）'
    )
    # 提供转字典方法
    def to_dict(self):
        return {
            "petal_id": self.petal_id,
            "flower_id": self.flower_id,
            "petal_length": self.petal_length,
            "petal_width": self.petal_width,
            "petal_ratio": self.petal_ratio,
            "petal_area": self.petal_area
        }
    # 表属性定义
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci',
        'comment': '花瓣形态参数表'
    }

# 花瓣形态数据校验
class PetalSchema(Schema):
    flower_id = fields.Int(required=True)
    petal_length = fields.Decimal(required=True, validate=validate.Range(min=0.1))
    petal_width = fields.Decimal(required=True, validate=validate.Range(min=0.1))
    petal_area = fields.Decimal(validate=validate.Range(min=0.1))