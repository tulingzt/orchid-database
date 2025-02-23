from app import db

# 花瓣形态模型定义
class PetalMorphology(db.Model):
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
    # 表属性定义
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci',
        'comment': '花瓣形态参数表'
    }
    # 对象的初始化
    def __init__(self, flower_id, petal_length, petal_width, petal_area):
        self.flower_id = flower_id
        self.petal_length = petal_length
        self.petal_width = petal_width
        self.petal_area = petal_area
    # 对象的标准字符串表示
    def __repr__(self):
        return f'<PetalMorphology {self.petal_id}>'