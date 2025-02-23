from app import db

# 萼片形态模型定义
class SepalMorphology(db.Model):
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
    # 表属性定义
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci',
        'comment': '萼片形态参数表'
    }
    # 对象的初始化
    def __init__(self, flower_id, sepal_length, sepal_width, sepal_area):
        self.flower_id = flower_id
        self.sepal_length = sepal_length
        self.sepal_width = sepal_width
        self.sepal_area = sepal_area
    # 对象的标准字符串表示
    def __repr__(self):
        return f'<SepalMorphology {self.sepal_id}>'