class DebugConfig():
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:testpass@db/challenge'
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:testpass@localhost/challenge'
    SECRET_KEY = 'webchatroom'