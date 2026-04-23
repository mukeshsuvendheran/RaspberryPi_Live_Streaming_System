from flask import Blueprint, render_template, redirect, url_for, request, session
from utils import get_config
from services.device_api_services import API
from services.group_services import Group
from services.device_services import Device
from models.motionCamera import MotionCamera
from db.database import Database
devices_bp = Blueprint("devices", __name__, url_prefix="/devices")

@devices_bp.route("/")
def devices_home():
    devices = Device.get_devices()
    return render_template('devices.html', session=session, devices=devices)

@devices_bp.route("/mcamera/<id>")
def devices_mcamera(id):
    dev = MotionCamera(id)
    db = Database.get_connection()
    result = db.motion_capture.find_one({
        "device_id": id,
        "owner": session.get('username')
    }, sort=[
        ("time", -1)
    ])
    return render_template('devices/mcamera.html', device=dev, latest=result['faccess']['get_url'])

@devices_bp.route("/add")
def devices_add():
    return render_template('devices/add.html', session=session, apis=API.get_all_keys(session, True), dtypes=get_config('devices'))