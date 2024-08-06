from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    users = {}

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)
        User.users[username] = self

    @staticmethod
    def get(username):
        return User.users.get(username)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username
