class DebugConfig():
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:testpass@db/challenge'
    # testpass 你的mysql的密码
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:testpass@localhost/challenge'
    SECRET_KEY = 'webchatroom'