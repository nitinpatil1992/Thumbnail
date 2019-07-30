import os

class Config(object):
    APP_DIR = os.path.abspath(os.path.dirname(__name__))
    IMAGE_FILES_DIR = '/data/'
    UPLOAD_FILE_SIZE_LIMIT = '1048576'
    UPLOAD_FILE_EXTENSIONS = ['png']
    THUMBNAIL_PROCESSING_STATUS = 'PROCESSING'
    THUMBNAIL_COMPLETED_STATUS = 'COMPLETED'    
    THUMBNAIL_FAILED_STATUS = 'FAILED'
    RABBITMQ_MSG_QUEUE = 'ImageConverter'
    HOST_BASENAME = "localhost"
    HOST_PORT = "5000"

class ProdConfig(Config):
    ENV = 'prod'
    DEBUG = False
    REDIS_HOST= 'redishost' 
    REDIS_PORT= 6379
    RABBITMQ_HOST = 'rabbitmqhost'

class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    REDIS_HOST = 'dev_redishost' #127.0.0.1
    REDIS_PORT = 6379
    RABBITMQ_HOST = 'dev_rabbitmqhost'

class TestConfig(Config):
    ENV = 'test'
    DEBUG = True
    REDIS_HOST = 'test_redishost'
    REDIS_PORT = 6379
    RABBITMQ_HOST = 'test_rabbitmqhost'