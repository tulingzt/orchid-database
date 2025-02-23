from app import db

# 兰花种类模型定义
class OrchidSpecies(db.Model):
    # 表名定义
    __tablename__ = 'orchid_species'
    # 表项定义
    species_id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True,
        comment = '物种唯一ID'
    )
    family = db.Column(
        db.String(50),
        nullable = False,
        comment = '科名（如兰科）'
    )
    genus = db.Column(
        db.String(50),
        nullable = False,
        comment = '属名（如石斛属）'
    )
    scientific_name = db.Column(
        db.String(100),
        unique = True,
        nullable = False,
        comment = '学名'
    )
    chinese_name = db.Column(
        db.String(100),
        unique = True,
        nullable = False,
        comment = '中文名'
    )
    distribution = db.Column(
        db.Text,
        comment = '地理分布信息'
    )
    conservation_status = db.Column(
        db.Enum('无危', '易危', '濒危', name = 'conservation_status'),
        nullable = False,
        default = '无危',
        comment = '保护级别'
    )
    # 表属性定义
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci',
        'comment': '兰花种类信息表'
    }
    # 对象的初始化
    def __init__(self, family, genus, scientific_name, chinese_name, distribution, conservation_status):
        self.family = family
        self.genus = genus
        self.scientific_name = scientific_name
        self.chinese_name = chinese_name
        self.distribution = distribution
        self.conservation_status = conservation_status
    # 对象的标准字符串表示
    def __repr__(self):
        return f'<OrchidSpecies {self.chinese_name}>'