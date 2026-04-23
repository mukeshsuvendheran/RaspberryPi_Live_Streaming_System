from flask import Blueprint, render_template, redirect, url_for, request, session
from src.user import User
from src.session import Session
from src.Device import Device
from src.devices.MotionCamera import MotionCamera
from src.API import API
from src.database import Database
from src import get_config
bp = Blueprint("devices", __name__, url_prefix="/devices")

@bp.route("/")
def devices_home():
    devices = Device.get_devices()
    return render_template('devices.html', session=session, devices=devices)

@bp.route("/mcamera/<id>")
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

@bp.route("/add")
def devices_add():
    return render_template('devices/add.html', session=session, apis=API.get_all_keys(session, True), dtypes=get_config('devices'))