from . import db
from .util import security
from flask_login import UserMixin
import re


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String, default="visitor")
    files = db.relationship("File", backref="user")
    folders = db.relationship("Folder", backref="user")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_email(self) -> str:
        return security.decrypt(self.email)

    def validate_pwd(self, pwd: str) -> bool:
        return security.check_pwd(pwd, self.password)

    @staticmethod
    def get_by_email(email: str):
        u = list(filter(lambda x: x.get_email() == email, User.query.all()))
        return None if len(u) == 0 else u[0]

    @staticmethod
    def check_allowed_register(email: str) -> bool:
        return not not re.fullmatch("\\w{5,}@\\w{3,}\\.\\w{2,4}", email) if not User.get_by_email(email) else False

    @staticmethod
    def new(email: str, password: str):
        email = security.encrypt(email)
        password = security.enc_pwd(password)
        u = User(email=email, password=password)
        u.save()
        return u


class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    mimetype = db.Column(db.String)
    bytes_size = db.Column(db.Integer)
    human_size = db.Column(db.String)
    path = db.Column(db.String)
    abs_path = db.Column(db.String)
    uid = db.Column(db.Integer, db.ForeignKey("users.id"))
    folder_id = db.Column(db.Integer, db.ForeignKey("folders.id"))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "mimetype": self.mimetype,
            "bytes_size": self.bytes_size,
            "human_size": self.human_size,
            "path": self.path,
            "abs_path": self.abs_path,
            "user": {
                "id": self.user.id,
                "id_from_file": self.uid,
                "email": self.user.get_email(),
                "avatar_url": "/avatar?email=" + self.user.get_email()
            }
        }


class Folder(db.Model):
    __tablename__ = "folders"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    path = db.Column(db.String)
    abs_path = db.Column(db.String)
    uid = db.Column(db.Integer, db.ForeignKey("users.id"))
    files = db.relationship("File", backref="folder")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def add_file(self, f: File):
        self.files.append(f)
        f.folder_id = self.id
        f.save()
        self.save()

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "path": self.path,
            "abs_path": self.abs_path,
            "user": {
                "id": self.user.id,
                "id_from_file": self.uid,
                "email": self.user.get_email(),
                "avatar_url": "/avatar?email=" + self.user.get_email()
            }
        }
