from flask import Blueprint
from app.controllers.paths_controller import create_path, delete_path, get_all_paths, get_paths_by_user_id, update_path


bp = Blueprint('bp_path', __name__, url_prefix='/paths')

bp.post('')(create_path)
bp.delete('/<int:id>')(delete_path)
bp.patch('/<int:id>')(update_path)
bp.get('')(get_all_paths)
bp.get('/<int:id>')(get_paths_by_user_id)