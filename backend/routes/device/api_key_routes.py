#api key routes
from flask import Blueprint, request, session
from services.device_api_services import API




device_bp = Blueprint("apiv1", __name__, url_prefix="/api/v1/")


@device_bp.route("/create/key", methods=['POST'])
def generate_api_key():
   name = request.form['name']
   group = request.form['group']
   remarks = request.form['remarks']
   
   if session.get('authenticated'): #TODO: Need more validattion like login expiry
      a = API.register_api_key(session, name, group, remarks)
      return {
         "key": str(a.collection.id),
         "hash": str(a.collection.hash),
         "message": "Success"
      }, 200
   else:
      return {
         "message": "Not Authenticated",
      }, 401