from flask import current_app as app
import os, json, uuid
import pika

def file_validation(ext, file_size):
    if ext not in app.config["UPLOAD_FILE_EXTENSIONS"]:
        return False
    if file_size == 0 or file_size > app.config["UPLOAD_FILE_SIZE_LIMIT"]:
        return False
    return True

def generate_image_path(uid, fileExtension):
    return app.config['IMAGE_FILES_DIR'] + uid + '.' + fileExtension

def get_uuid():
    return str(uuid.uuid4())

def publish_to_queue(message={}):
    msg_queue = app.config['RABBITMQ_MSG_QUEUE']
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=app.config['RABBITMQ_HOST']))
    channel = connection.channel()
    channel.queue_declare(queue=msg_queue, durable=True)
    channel.basic_publish(exchange='', routing_key=msg_queue, body=json.dumps(message))
    connection.close()

def generate_imagelinks(image_path):
    basename = os.path.basename(os.path.normpath(image_path))
    return 'http://' + app.config['HOST_BASENAME'] + ':' + app.config['HOST_PORT'] + '/image/' + basename 