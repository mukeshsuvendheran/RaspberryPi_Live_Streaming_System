from flask import Blueprint, render_template, redirect, url_for, request, session
from services.group_services import Group

bp = Blueprint("apiv1", __name__, url_prefix="/api/v1/")

 
@bp.route("/create/group", methods=['POST'])
def create_group():
   name = request.form['name']
   description = request.form['description']
   if(len(name) < 3) or (len(description) < 3):
      return {
         "message": "Name and Description must be atleast 3 characters",
      }, 400
   if session.get('authenticated'): #TODO: Need more validattion like login expiry
      Group.register_group(name, description)
      return {
         "status": "success",
         "message": "Successfully created group " + name,
      }, 200
   else:
      return {
         "message": "Not Authenticated",
      }, 401
      