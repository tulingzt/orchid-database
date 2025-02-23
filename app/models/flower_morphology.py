from app import db

# 花朵形态模型定义
class FlowerMorphology(db.Model):
    # 表名定义
    __tablename__ = 'flower_morphology'
    # 表项定义
    flower_id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True,
        comment = '花朵数据ID'
    )
    species_id = db.Column(
        db.Integer,
        db.ForeignKey('orchid_species.species_id', ondelete = 'CASCADE', onupdate = 'CASCADE'),
        nullable = False,
        comment = '关联物种ID',
        index = True
    )
    flower_length = db.Column(
        db.DECIMAL(6, 2),
        nullable = False,
        comment = '花朵长度（cm）'
    )
    flower_width = db.Column(
        db.DECIMAL(6, 2),
        nullable = False,
        comment = '花朵宽度（cm）'
    )
    flower_ratio = db.Column(
        db.DECIMAL(6, 2),
        db.Computed('flower_length / flower_width'),
        comment = '长宽比（自动计算）'
    )
    flower_area = db.Column(
        db.DECIMAL(8, 2),
        comment = '花朵整体面积（cm²）'
    )
    # 表属性定义
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci',
        'comment': '花朵形态参数表'
    }
    # 对象的初始化
    def __init__(self, species_id, flower_length, flower_width, flower_area):
        self.species_id = species_id
        self.flower_length = flower_length
        self.flower_width = flower_width
        self.flower_area = flower_area
    # 对象的标准字符串表示
    def __repr__(self):
        return f'<FlowerMorphology {self.flower_id}>'