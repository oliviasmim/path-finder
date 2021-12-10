from flask import Blueprint
from app.controllers.user_controller import create_user, delete_user, get_all_users, login, get_by_username, update_user

bp = Blueprint('bp', __name__)

bp.post('/signup')(create_user)
bp.post('/login')(login)
bp.get('/users')(get_all_users)
bp.get('/user/<int:id>')(get_by_username)
bp.patch('/user/<int:id>')(update_user)
bp.delete('/user/<int:id>')(delete_user)
