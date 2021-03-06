from sqlalchemy.orm import backref
from app.configs.database import db
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash
from app.exceptions.base_exceptions import EmptyStringError, InvalidPasswordLength, MissingKeyError, NotFoundDataError, NotStringError, UserOwnerError, WrongKeysError, EmailAlreadyExists, UsernameAlreadyExists, PasswordConfirmationDontMatch
from datetime import datetime, timezone

@dataclass
class UserModel(db.Model):
    id: int
    name: str
    username: str
    email: str
    birthdate: str
    url_image: str
    created_at: str
    updated_at: str
    paths_list: list

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirm_email = db.Column(db.Boolean, default=False)
    birthdate = db.Column(db.DateTime(timezone=True), nullable=False)
    url_image = db.Column(db.String)
    password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    paths_list = db.relationship('PathModel', backref=backref('user', uselist=False))


    @property
    def password(self):
        raise AttributeError('Wrong password.')

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def verify_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)
    
    @staticmethod
    def validate(**kwargs):
        valid_keys = ['name', 'username', 'email', 'birthdate', 'url_image', 'password', 'password_confirmation']
        required_keys = ['name', 'username', 'email', 'birthdate', 'password', 'password_confirmation']
        received_keys = [key for key in kwargs.keys()]

        for key in received_keys:
            if key not in valid_keys:
                raise WrongKeysError(valid_keys, received_keys)
            
            if not type(kwargs[key]) == str:
                raise NotStringError(f'{key} must be string!')

        for key in required_keys:
            if not key in received_keys:
                raise MissingKeyError(required_keys, key)

            if kwargs[key] == '':
                raise EmptyStringError(f'{key} must not be an empty string!')
        
        password_confirmation = kwargs.pop('password_confirmation')
        if not kwargs['password'] == password_confirmation:
            raise PasswordConfirmationDontMatch('Password and Password Confirmation must be equal.')
        
        found_user_email: UserModel = UserModel.query.filter_by(email=kwargs['email']).first()
        found_user_username: UserModel = UserModel.query.filter_by(username=kwargs['username']).first()
        
        if found_user_username:
            raise UsernameAlreadyExists('this username already exists!')

        if found_user_email:
            raise EmailAlreadyExists('this email already exists!')

        if len(kwargs['password']) < 8:
            raise InvalidPasswordLength('your password must have at least 8 characters!')

        kwargs['name'] = kwargs['name'].title()

        return kwargs

    @staticmethod
    def validate_update(**kwargs):
       
        if 'username' in kwargs.keys():
            found_user_username: UserModel = UserModel.query.filter_by(username=kwargs['username']).first()
            if found_user_username:
                raise UsernameAlreadyExists('this username already exists!')
            
        if 'email' in kwargs.keys():
            found_user_email: UserModel = UserModel.query.filter_by(email=kwargs['email']).first()
            if found_user_email:
                raise EmailAlreadyExists('this email already exists!')

        return kwargs

    @staticmethod
    def validate_user(current_id, user_id):
        user = UserModel.query.get(user_id)

        if not user:
            raise NotFoundDataError('User ID not Found')

        if not user.id == current_id:
            raise UserOwnerError('you cannot update or delete a different user!')
        
        return current_id, user_id
