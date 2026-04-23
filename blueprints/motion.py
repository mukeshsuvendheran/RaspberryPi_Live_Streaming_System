from flask import Blueprint, render_template, redirect, url_for, request, session
from src.API import API
from src.devices.MotionCamera import MotionCamera
from gridfs import GridFS, GridFSBucket
from src.database import Database
import mimetypes
import uuid

bp = Blueprint("motion", __name__, url_prefix="/api/motion/")

@bp.route("/capture", methods=['POST'])
def capture_motion():
    if 'file' in request.files and session.get('authenticated'):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            print(auth_token)
            api = API(auth_token)
            device = api.get_device()  
            device_id = device['id']
            file = request.files['file']
            fs = GridFSBucket(Database.get_connection())
            
            metadata = {
                'original_filename': file.filename,
                'content_type': mimetypes.guess_type(file.filename)[0],
                'owner': session.get('username'),
                'device_id': device_id
            }
            
            filename = str(uuid.uuid4())
            
            file_id = fs.upload_from_stream(filename, file, metadata=metadata)
            mc = MotionCamera(device_id)
            
            faccess = {
                'message': "Upload Success",
                'file_id': str(file_id),
                'filename': filename,
                'download_url': '/files/download/'+filename,
                'stream_url': '/files/stream/'+filename,
                'get_url': '/files/get/'+filename,
                'type': 'success'
            }
            mc.save_capture(file_id, faccess)
            return faccess, 200
    else:
        return {
            'message': 'Bad Request',
            'type': 'error'
        }, 400

@bp.route('/latest/<id>')
def latest_motion_capture(id):
    db = Database.get_connection()
    result = db.motion_capture.find_one({
        "device_id": id,
        "owner": session.get('username')
    }, sort=[
        ("time", -1)
    ])

    if result:
        return {
            "uri": result['faccess']['get_url']
        }
    else:
        return {
            "error": "Cannot find"
        }

