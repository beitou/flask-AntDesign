import os

from app.tasks.task_jobs import job_1

basedir = os.path.abspath(os.path.dirname(__file__))

TEAM_DICT = {
    "3": "基础服务",
    "5": "财商基金",
    "4": "保险服务",
    "6": "保险供应链",
    "7": "数据平台",
    "9": "系统运维",
    "44": "大前端",
    "8": "实例项目",
    "29": "设计"
}

class Config:
    DEBUG=True
    # 如何生成强壮的密钥，首先import os,然后os.urandom(24)即可
    SECRET_KEY = 'jcl_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = 'qa@xiaobangtouzi.com'
    # FLASKY_MAIL_SENDER = 'jcl_send'
    # FLASKY_ADMIN = 'jcl_admin'
    LDAP_HOST = "ldaps://ad01.xiaobang.xyz"
    LDAP_ADMIN = {
        "user": "wechat_sync@xiaobang.xyz",
        "pwd": "JWPRj7pa^J#3NLZ3"
    }
    WECHAT_CONFIG = {
        "corp_id": "wwf1143b4d1547c208",
        "corp_secret": "IyrzR40w1pK2nVWEYIxWCQ9LkOWw7Wrcf45PTEubbV4"
    }
    GIT_SERVER="http://code.xiaobangtouzi.com/"
    JIRA_SERVER="http://jira.xiaobangtouzi.com/"

    #新增一个APS的API的开关
    SCHEDULER_API_ENABLED = True
    SQLALCHEMY_ECHO = True

    # 注意：需要定时执行的job只需要在这添加配置！
    JOBS = [
      {
          'id': 'jcl_0109_job001',
          'func': job_1,
          'args': None,
          'trigger': {
              'type': 'cron', # 类型
              'day_of_week': "0-6",	# 可定义具体哪几天要执行
              'hour': '22',	# 小时数
              'minute': '0'
          }
      }
      # {
      #   'id': 'jcl_0109_job002',
      #   'func': job_1,
      #   'args': '',
      #   'trigger': 'interval',
      #   'seconds': 5  # 每隔5秒执行一次
      # },
      # {
      # 	'id': 'jcl_0109_job003',
      # 	'func': 'job_1',
      #   # 一次性任务可以省略trigger
      # 	'args': None,
      # 	'next_run_time': datetime.datetime.now() + datetime.timedelta(seconds=10)
      # }
    ]

    @staticmethod # 可以使用类名直接调用该方法
    def init_app(app): #执行当前需要的环境的初始化
        return u'环境初始化成功'


# 开发环境
class DevelopmentConfig(Config):
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    # MAIL_USERNAME = 'qa@xiaobangtouzi.com'
    # MAIL_PASSWORD = '3fEJS7CcrxQSGALK'
    MAIL_USERNAME = 'jiangchenglong@xiaobangtouzi.com'
    MAIL_PASSWORD = '3fEJS7CcrxQSGALK'
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:123456a@127.0.0.1:3306/quality?charset=utf8"
    SQLALCHEMY_POOL_RECYCLE = 3599
    SQLALCHEMY_MAX_OVERFLOW = 100
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO")
    '''
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = '123456a'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'quality'

    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}'.format(
        DIALECT,
        DRIVER,
        USERNAME,
        PASSWORD,
        HOST,
        PORT,
        DATABASE
    )
    # 便于调试
    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    '''
    JIRA_SERVER="http://jira.xiaobangtouzi.com/"


# 测试环境
class TestingConfig(Config):
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    # MAIL_USERNAME = 'qa@xiaobangtouzi.com'
    # MAIL_PASSWORD = '3fEJS7CcrxQSGALK'
    MAIL_USERNAME = 'jiangchenglong@xiaobangtouzi.com'
    MAIL_PASSWORD = '3fEJS7CcrxQSGALK'
    QUALITY_DATABASE = {
        'host': '172.16.0.115',
        'port': 3306,
        'user': 'quality_qa',
        'pswd': '#UE3a=jBaNnDqtGt',
        'db':'quality',
        'charset': 'utf8'
    }
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{user}:{pswd}@{host}:{port}/{db}?charset={charset}".format(**QUALITY_DATABASE)
    # 需要关联其他数据库表，在下方添加
    SQLALCHEMY_BINDS = {
        'xb':'mysql+mysqlconnector://{user}:{pswd}@{host}:{port}/{db}?charset={charset}'.format(**QUALITY_DATABASE)
    }
    SQLALCHEMY_POOL_RECYCLE = 3599
    SQLALCHEMY_MAX_OVERFLOW = 100
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO")
    # 这个是莞羚的QA验证码业务
    CATPCHA = {
      'host': '172.16.0.115',
      'port': 3306,
      'user': 'app',
      'password': 'Yc)E7aqYU6)AjW',
      'database': 'user_center',
      'charset': 'utf8'
    }
    JIRA_SERVER = "http://jira.xiaobangtouzi.com:8080/"


# 生产环境
class ProductionConfig(Config):
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'jiangchenglong@xiaobangtouzi.com'
    MAIL_PASSWORD = '3fEJS7CcrxQSGALK'
    QUALITY_DATABASE = {
        'host': '172.16.236.11',
        'port': 3306,
        'user': 'quality',
        'pswd': '6A5mK232t17w',
        'db':'quality',
        'charset': 'utf8'
    }
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{user}:{pswd}@{host}:{port}/{db}?charset={charset}".format(**QUALITY_DATABASE)
    # 需要关联其他数据库表，在下方添加
    SQLALCHEMY_BINDS = {
        'xb':'mysql+mysqlconnector://{user}:{pswd}@{host}:{port}/{db}?charset={charset}'.format(**QUALITY_DATABASE)
    }
    SQLALCHEMY_POOL_RECYCLE = 3599
    SQLALCHEMY_MAX_OVERFLOW = 100
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO")
    # 这个是莞羚的验证码业务
    CATPCHA = {
      'host': '172.16.16.49',
      'port': 3306,
      'user': 'user_center_read',
      'password': 'V@C^jJfdJe9FLhtV',
      'database': 'user_center',
      'charset': 'utf8'
    }


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': TestingConfig
}
