from flask import Blueprint, render_template, redirect, url_for, request, session
from utils import get_config
from services.device_api_services import API
from services.device_services import Device 
import time
import uuid


devices_auth_bp = Blueprint("devices_api", __name__, url_prefix="/api/devices")

@devices_auth_bp.route("/register", methods=['POST'])
def devices_add():
    if session.get('authenticated') and 'name' in request.form and 'type' in request.form and 'api' in request.form and 'remarks' in request.form:
        name = request.form['name']
        dtype = request.form['type']
        api_key = request.form['api']
        remarks = request.form['remarks']
        return_json = 'json' in request.form
        
        if len(name) < 3:
            return {
                "error": "Name too short",
            }, 400
        
        if len(remarks) < 3:
            return {
                "error": "Remarks too short",
            }, 400
        
        valid_dtype = False
        dtypes = get_config("devices")
        for _type in dtypes:
            if _type['id'] == dtype:
                valid_dtype = True
                break
        
        if not valid_dtype:
            return {
                "error": "Invalid Device Type",
            }, 400
        
        api = API(api_key)
        if(api.is_valid()):
            dev = Device.register_device(name, session.get('username'), dtype, api_key, remarks);
            if return_json:
                return {
                    "message": "Device Registered",
                    "id": dev.uuid
                }
            else:
                return render_template('devices/card.html', device=dev.collection)
        else:
            return {
                "error": "Invalid API Key",
            }, 400

    else:
        return {
            "error": "Bad Request",
        }, 400