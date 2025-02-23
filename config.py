# 设置连接数据库的信息
HOSTNAME = '127.0.0.1'
PORT = 3306
USERNAME = 'root'
PASSWORD = '123456'
# DATABASE='orchid_morphology_database'
DATABASE='test'

# 真正被调用的配置
class Config:
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False