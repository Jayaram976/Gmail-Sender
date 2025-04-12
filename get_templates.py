# get_templates.py
from flask import Blueprint, jsonify

get_templates_bp = Blueprint('get_templates', __name__)

@get_templates_bp.route('/get_templates')
def get_templates():
    templates = ["Interview Invite", "Offer Letter", "Follow Up"]
    return jsonify(templates)
