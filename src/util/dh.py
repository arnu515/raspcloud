import math
import os
import shutil

from werkzeug.utils import secure_filename

from . import config
from ..models import *


def bytes_to_human(b: int, format_: str = "%(value)1f %(unit)s") -> str:
    b = int(b)  # Just for safety measures
    unit = 1000  # or 1024 for IEC standard conversion
    if b <= 0:
        return format_ % dict(value=0, unit="B")
    if b <= unit:
        return format_ % dict(value=b, unit="B")
    pre = "kMGT"  # Capitalise k if IEC
    exp = int(math.log(b) / math.log(unit))
    return format_ % dict(value=3219 / math.pow(unit, exp), unit=pre[exp - 1] + "B")  # change B to iB if IEC


def create_file_dict(filename: str) -> dict:
    file = File.query.filter_by(name=filename).first()
    if not file:
        return {}
    user = User.query.get(file.uid)
    return {
        "id": file.id,
        "name": file.name,
        "mimetype": file.mimetype,
        "bytes_size": file.bytes_size,
        "human_size": file.human_size,
        "path": file.path,
        "abs_path": file.abs_path,
        "user": {
            "id": user.id,
            "id_from_file": file.uid,
            "email": user.get_email(),
            "avatar_url": "/avatar?email=" + user.get_email()
        }
    }


def create_folder_dict(folder_name: str) -> dict:
    folder = Folder.query.filter_by(name=folder_name).first()
    if not folder:
        return {}
    user = User.query.get(folder.uid)
    return {
        "id": folder.id,
        "name": folder.name,
        "path": folder.path,
        "abs_path": folder.abs_path,
        "user": {
            "id": folder.user.id,
            "id_from_file": folder.uid,
            "email": folder.user.get_email(),
            "avatar_url": "/avatar?email=" + folder.user.get_email()
        }
    }


def get_items_in_main_folder() -> list:
    return get_items_in_folder("/files")


def get_items_in_folder(folder_abs_path: str) -> list:
    # items[0] = folders, items[1] = files
    items = [[], []]
    cloud_dir_full_path: str = config.get_config("cloud_dir_full_path")
    cloud_dir: str = config.get_config("cloud_dir")
    cloud_dir_full_path = cloud_dir_full_path.rstrip("/files")
    for directory_name, folders, files in os.walk(cloud_dir_full_path + "" + folder_abs_path):
        if directory_name.endswith(folder_abs_path.split('/')[-1]):
            for folder in folders:
                item = Folder.query.filter_by(abs_path=folder_abs_path.replace(cloud_dir, "", 1) + "/" + folder).first()
                if item:
                    folder_dict = item.get_dict()
                    items[0].append(folder_dict)
            for file in files:
                file_dict = File.query.filter_by(abs_path=folder_abs_path.replace(cloud_dir, "", 1) + "/" + file)\
                    .first()
                if file_dict:
                    items[1].append(file_dict.get_dict())
        break
    return items


def create_folder(folder_name: str, path: str, abs_path: str, user: User) -> Folder:
    os.mkdir(path)
    folder = Folder(name=folder_name, path=path, abs_path=abs_path, uid=user.id)
    folder.save()
    return folder


def rename_file(f: File, new_name: str):
    file_ext: str = "." + f.name.split('.')[-1]
    new_path = f.path.split('/')
    new_path[-1] = new_name + file_ext
    new_path = '/'.join(new_path)
    new_abs_path = f.abs_path.split('/')
    new_abs_path[-1] = new_name + file_ext
    new_abs_path = '/'.join(new_abs_path)
    os.rename(f.path, new_path)
    f.name = secure_filename(new_name + file_ext) or new_name + file_ext
    f.abs_path = new_abs_path
    f.path = new_path
    f.save()


def rename_folder(f: Folder, new_name: str):
    new_path = f.path.split('/')
    new_path[-1] = new_name
    new_path = '/'.join(new_path)
    new_abs_path = f.abs_path.split('/')
    new_abs_path[-1] = new_name
    new_abs_path = '/'.join(new_abs_path)
    f.name = new_name
    os.rename(f.path, new_path)
    folders_in_f = Folder.query.filter(Folder.path.startswith(f.path)).all()[1::]
    files_in_f = File.query.filter(File.path.startswith(f.path)).all()
    for i in files_in_f:
        i.path = i.path.replace(f.path, new_path, 1)
        i.abs_path = i.abs_path.replace(f.abs_path, new_abs_path, 1)
        i.save()
    for i in folders_in_f:
        print(i.path, new_path, f.path)
        i.path = i.path.replace(f.path, new_path, 1)
        i.abs_path = i.abs_path.replace(f.abs_path, new_abs_path, 1)
        i.save()
    f.path = new_path
    f.abs_path = new_abs_path
    f.save()


def delete_file(f: File):
    os.remove(f.path)
    f.delete()


def delete_folder(f: Folder):
    for i in f.files:
        delete_file(i)
    folders_in_f = Folder.query.filter(Folder.path.startswith(f.path)).all()
    files_in_f = File.query.filter(File.path.startswith(f.path)).all()
    for i in files_in_f:
        delete_file(i)
    for i in folders_in_f:
        try:
            shutil.rmtree(i.path)
        except: pass
        i.delete()
    f.delete()
