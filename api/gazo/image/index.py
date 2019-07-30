from flask import Flask, Blueprint, request, jsonify, send_from_directory, current_app as app
from gazo import utils, extensions, exceptions
from collections import OrderedDict
import os, uuid, mimetypes

image = Blueprint('image', __name__, url_prefix='/image')

@image.route('/', methods=['POST'])
def upload():
    f = request.files['file']
    file_extension = f.filename.rsplit('.', 1)[1].lower()

    uid = utils.get_uuid()
      = utils.generate_image_path(uid, file_extension)
    f.save(image_path)
    
    if not utils.file_validation(file_extension, os.stat(image_path).st_size):
        raise exceptions.InvalidUsage('Bad request', status_code=400)
    
    try:
        image_data = {
            'image_id'   : uid,
            'image_ext'  : file_extension,
            'image_path' : image_path
        }
        extensions.redis.hmset(uid, image_data)
        
        utils.publish_to_queue({'image_id': uid})
        
        # once published image_id to queue, set thumbnail status to processing in db store
        extensions.redis.hset(uid, 'thumbnail_status' , app.config['THUMBNAIL_PROCESSING_STATUS'])
    except Exception:
        raise exceptions.InvalidUsage('Internal Server Error, Try again later', status_code=503)
    
    return jsonify({'request_id': uid})

@image.route('/<string:image_basename>', methods=['GET'])
def get_image(image_basename):
    file_path = app.config['IMAGE_FILES_DIR'] +  image_basename

    if not os.path.isfile(file_path):
        raise exceptions.InvalidUsage('File not found', status_code=404)

    mime_type=mimetypes.MimeTypes().guess_type(file_path)[0]
    return send_from_directory(app.config['IMAGE_FILES_DIR'],image_basename,mimetype=mime_type)

@image.route('/<string:request_id>/thumbnail', methods=['GET'])
def get_thumbnail_status(request_id):
    try:
        image_data = extensions.redis.hgetall(request_id)
        if not image_data:
            raise ValueError('No data')
    except ValueError:
        raise exceptions.InvalidUsage('No such request registered in system', status_code=404)
    except Exception:
        raise exceptions.InvalidUsage('Internal Server Error, Try again later', status_code=503)

    image_conversion_status = image_data['thumbnail_status']
    
    response = OrderedDict()
    response['request_id'] = request_id
    response['thumbnail_status'] = image_conversion_status
    
    if image_conversion_status == app.config['THUMBNAIL_COMPLETED_STATUS']:
        response['result'] = {
            'original_image' : utils.generate_imagelinks(image_data['image_path']),
            'thumbnail_100x100' : utils.generate_imagelinks(image_data['thumbnail_path'])
        }
    
    return jsonify(response), 200
