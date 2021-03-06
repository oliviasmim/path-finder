from flask import Blueprint
from app.controllers.activities_controller import create_activity, delete_activity, update_activity, activities_by_point
from app.routes.reviews_blueprint import bp as bp_reviews

bp = Blueprint('bp_activities', __name__, url_prefix='/points')

bp.post('/activities')(create_activity)
bp.get('/<int:point_id>/activities')(activities_by_point)
bp.patch('/activities/<int:id>')(update_activity)
bp.delete('/activities/<int:id>')(delete_activity)
bp.register_blueprint(bp_reviews, url_prefix='/activities')
