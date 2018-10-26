import os

class Config(object):
    # Clase padre de config
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')

    API_REST_PORT = 5000
    API_SOAP_PORT = 5010
    HOST_GDS_SOAP_API = 'http://127.0.0.1:'+str(API_SOAP_PORT)+'/'
    HOST_GDS_REST_API = 'http://127.0.0.1:'+str(API_REST_PORT)+'/'
    GLOBAL_NAMESPACE = HOST_GDS_SOAP_API + 'cnet/flight/'
    STRUCTURE_NAMESPACE = HOST_GDS_SOAP_API + 'cnet/structure/'

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    # Clase dev
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/transoft_test'


class TestingConfig(Config):
    # Clase de testing
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'
    DEBUG = True


class StagingConfig(Config):

    DEBUG = True


class ProductionConfig(Config):

    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
