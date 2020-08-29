import os
import re
from urllib.parse import urlparse, urljoin

from flask import current_app as app, render_template, request, redirect, url_for, flash, jsonify, make_response, abort, \
    send_from_directory
from werkzeug.utils import secure_filename as sf
from flask_login import current_user, login_user, login_required, logout_user
from . import lm
from .models import User, Folder, File
from .util import config, dh
from .util.avatar import Avatar


@lm.user_loader
def user_loader(uid):
    return User.query.get(uid)


@lm.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for("index"))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


if app.config["INSTALLED"]:
    @app.route('/')
    def index():
        if not current_user.is_authenticated:
            return render_template("not_logged_in.html")
        else:
            return render_template("index.html", items=dh.get_items_in_main_folder())


    @app.route('/<path:folder_path>')
    def folder_route(folder_path: str):
        if not current_user.is_authenticated:
            return redirect(url_for("index"))
        else:
            if not Folder.query.filter_by(abs_path="/" + folder_path).first():
                flash("The specified folder doesn't exist", "error")
                return redirect(url_for("index"))
            return render_template("index.html", items=dh.get_items_in_folder("/files/" + folder_path))


    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return redirect(url_for("index"))
        else:
            email: str = request.form.get("email")
            password: str = request.form.get("password")
            if not email or not password:
                flash("Enter a valid email and password (400)", "error")
                return redirect(url_for("index"))
            if not re.fullmatch("\\w{5,}@\\w{3,}\\.\\w{2,4}", email):
                flash("Enter a valid email", "error")
                return redirect(url_for("index"))
            u = User.get_by_email(email.lower())
            if not u:
                flash("Invalid credentials", "error")
                return redirect(url_for("index"))
            if u.validate_pwd(password):
                login_user(u)
                return redirect(url_for("index"))
            else:
                flash("Invalid credentials", "error")
                return redirect(url_for("index"))


    @app.route("/logout")
    def logout():
        if current_user.is_authenticated:
            logout_user()
        return redirect(url_for("index"))


    @app.route("/avatar")
    def generate_avatar():
        return make_response(Avatar.generate(32, request.args.get("email", "deleted"), "PNG"), 200,
                             {"Content-Type": "image/png"})


    @app.route("/new", methods=["POST"])
    @login_required
    def new():
        type_ = request.form.get("type")
        if not type_:
            return make_response(jsonify("Bad request"), 400)
        if type_ == "new_folder":
            path: str = request.form.get("path")
            folder_name: str = request.form.get("folder")
            if not path or not folder_name:
                flash("Invalid folder name!", "error")
                if is_safe_url(request.args.get("next")):
                    return redirect(request.args.get("next"))
                return redirect(url_for("index"))
            folder_name = folder_name.strip().replace("%20", " ")
            folder_name = sf(folder_name)
            path = path.rstrip().replace("%20", " ")
            if not path or not folder_name:
                flash("Invalid folder name!", "error")
                if is_safe_url(request.args.get("next")):
                    return redirect(request.args.get("next"))
                return redirect(url_for("index"))
            if not re.fullmatch(r"[\w_\s-]+", folder_name, re.I):
                flash("Invalid folder name!", "error")
                if is_safe_url(request.args.get("next")):
                    return redirect(request.args.get("next"))
                return redirect(url_for("index"))
            if not path.endswith("/"):
                path += "/"
            abs_path: str = path
            path = config.get_config("cloud_dir_full_path") + path + folder_name
            abs_path += folder_name
            try:
                dh.create_folder(folder_name, path, abs_path, current_user)
            except FileExistsError:
                flash("This folder already exists!", "error")
            if is_safe_url(request.args.get("next")):
                return redirect(request.args.get("next"))
            return redirect(url_for("index"))
        elif type_ == "upload_file":
            # If this doesn't work, then use this method:
            # - Instead of having a files array, just add all of the file inputs
            # to a div.w3 - hide and just make the form submit with action attribute
            # No need of fetch, or FormData
            # NOTE: You may need to add content - type = multipart / form - data
            # as attribute to form element
            temp_files_list = []
            if request.files:
                path = request.form.get("path")
                if len(path) == 0:
                    return make_response(jsonify("Invalid"), 400)
                path.replace("%20", " ")
                cloud_dir_full_path = config.get_config("cloud_dir_full_path")
                if path == "/":
                    path = ""
                for file_item in request.files:
                    file = request.files[file_item]
                    filename: str = sf(file.filename) or file.filename
                    file.save(cloud_dir_full_path + path + "/" + filename)
                    file_size = os.stat(cloud_dir_full_path + path + "/" + filename).st_size
                    temp_files_list.append(File(name=filename, path=cloud_dir_full_path + path + "/" + filename,
                                                abs_path=path + '/' + filename, mimetype=file.mimetype,
                                                bytes_size=file_size, human_size=dh.bytes_to_human(file_size),
                                                uid=current_user.id))
                print(path)
                if path == "":
                    path = "/"
                f: Folder = Folder.query.filter_by(abs_path=path).first()
                for i in temp_files_list:
                    f.add_file(i)
                return make_response(jsonify("All good"), 200)
        return make_response(jsonify("Invalid"), 400)


    @app.route("/dl/<path:filepath>")
    def download_file(filepath: str):
        return send_from_directory(config.get_config("cloud_dir_full_path"), filepath)


    @app.context_processor
    def add_utils_processor():
        def get_file_icon(mimetype: str) -> str:
            filetype = mimetype.split('/')
            if filetype[0] == "video":
                return "file-video"
            if filetype[0] == "audio":
                return "file-audio"
            if filetype[0] == "image":
                return "file-image"
            if mimetype == "application/pdf":
                return "file-pdf"
            if mimetype == "application/vnd.rar":
                return "file-archive"
            if mimetype == "application/zip":
                return "file-archive"
            if filetype[0] == "application":
                return "file"
            if filetype[0] == "font":
                return "file-signature"
            return "file"
        return dict(get_file_icon=get_file_icon)

else:

    @app.route('/')
    def index():
        logout_user()
        if app.config["INSTALLED"]:
            return "Installed successfully. Please restart the application"
        else:
            return "<h1>NOT INSTALLED/CONFIGURED PROPERLY</h1>" + \
                   "<a href=\"/install\">Please visit this page to install</a>"


    @app.route("/install", methods=["GET", "POST"])
    def install():
        logout_user()
        if request.method == "GET":
            if app.config["INSTALLED"]:
                return "Please restart the application"
            else:
                return render_template("install.html")
        else:
            if app.config["INSTALLED"]:
                return "Please restart the application"
            email: str = request.form.get("two-email")
            password: str = request.form.get("two-password")
            confirm_password: str = request.form.get("two-confirm-password")
            if not email or not password:
                flash("Enter a valid email and password (400)", "error")
                return redirect(url_for("install"))
            if not password == confirm_password:
                flash("Passwords don't match", "error")
                return redirect(url_for("install"))
            if not User.check_allowed_register(email):
                flash("Enter a valid email / Email already registered", "error")
                return redirect(url_for("install"))
            u = User.new(email, password)
            u.role = "main"
            config.set_config("main_acc", u.id)
            u.save()
            try:
                os.mkdir(os.getcwd() + "/files")
            except FileExistsError:
                pass
            folder = Folder(name="files", path=os.getcwd() + "/files",
                            abs_path="/", uid=u.id)
            folder.save()
            config.set_config("cloud_dir", "/files")
            config.set_config("cloud_dir_full_path", os.getcwd() + "/files")
            config.set_config("installed", True)
            app.config["INSTALLED"] = True
            return redirect(url_for("index"))
