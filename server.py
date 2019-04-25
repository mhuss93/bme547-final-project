from flask import Flask, jsonify, request
from pymodm.errors import ValidationError
import datetime
import database as db


app = Flask(__name__)


@app.route("/", methods=["GET"])
def server_on():
    return "image processor server is ON"


@app.route("/api/upload_user_image", methods=["POST"])
def handler_upload_user_images():
    """
    Uploads a new image for a given user.
    """

    r = request.get_json()
    try:
        user_id = r['user_id']
        filename = r['filename']
        extension = r['extension']
        image_str = r['image']
        message = db.upload_image(user_id, filename, extension, image_str)
        return jsonify(message), 200
    except ValidationError as e:
        return jsonify(e.message), 422
    except KeyError as e:
        errormessage = 'Field {} is missing.'.format(e)
        return jsonify(errormessage), 400
