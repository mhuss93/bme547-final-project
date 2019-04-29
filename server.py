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
    import datetime
    from encode_decode import imgArray2str, str2imgArray
    """
    Uploads a new image for a given user.
    """

    r = request.get_json()
    try:
        user_id = r['user_id']
        filename = r['filename']
        extension = r['extension']
        image_str = r['original_image']
        method = r['method']
        img = str2imgArray(image_str)
        if method != 'none':
            time = datetime.datetime.now()
            timetoprocess, proc_img = db.process_image(img, method)
            proc_img_str = imgArray2str(proc_img)
            message_up = db.upload_image(user_id, filename, extension,
                                         image_str)
            message_proc = db.save_processed_image(
                filename,
                proc_img_str,
                user_id,
                method,
                time,
                timetoprocess,
                extension
            )
        else:
            message_up = db.upload_image(user_id, filename, extension,
                                         image_str)
            message_proc = "No image manipulation performed."
            proc_img_str = None
        return_dict = {
            'upload_status': message_up,
            'processed_status': message_proc,
            'original_image': image_str,
            'processed_image': proc_img_str,
        }
        return jsonify(return_dict), 200
    except ValidationError as e:
        return jsonify(e.message), 422
    except KeyError as e:
        errormessage = 'Field {} is missing.'.format(e)
        return jsonify(errormessage), 400


@app.route("/api/register_user", methods=["POST"])
def handler_register_user():
    """
    Register a User on the database.
    """

    r = request.get_json()
    try:
        user_id = r['user_id']
        message = db.register_user(user_id)
        return jsonify(message), 200
    except ValidationError as e:
        return jsonify(e.message), 422
    except db.UserExists as e:
        return jsonify(e), 200
    except KeyError as e:
        errormessage = 'Field {} is missing.'.format(e)
        return jsonify(errormessage), 400


@app.route("/api/get_uploaded_image", methods=["POST"])
def handler_get_uploaded_image():
    """
    Retrieve an image from the database.
    """

    r = request.get_json()
    try:
        user_id = r['user_id']
        filename = r['filename']
        extension = r['extension']
        img_dict = db.get_uploaded_image(user_id, filename, extension)
        return jsonify(img_dict), 200
    except db.Image.DoesNotExist:
        out = 'Requested Image does not exist: {}, {}.{}'.format(user_id,
                                                                 filename,
                                                                 extension)
        return jsonify(out), 404
    except KeyError as e:
        errormessage = 'Field {} is missing.'.format(e)
        return jsonify(errormessage), 400


@app.route("/api/process_existing_image", methods=["POST"])
def handler_process_existing_image():
    """
    Process an image already on the server.
    """
    pass


@app.route("/api/get_processed_image", methods=["POST"])
def handler_get_processed_image():
    """
    Retrieve a processed image from teh database.
    """
    try:
        user_id = r['user_id']
        filename = r['filename']
        extension = r['extension']
        method = r['method']
        if not isinstance(method, list):
            method = [method]
        proc_image = db.ProcessedImage.objects.userprocessedimage(
            user_id,
            filename,
            extension,
            method
        )
        return_dict = {
            'img': proc_image.image,
            'filename': proc_image.filename,
            'extension': proc_image.extension,
            'method': proc_image.procedureType
        }
        return jsonify(return_dict), 200
    except KeyError as e:
        errormessage = 'Field {} is missing.'.format(e)
        return jsonify(errormessage), 400
    except db.ProcessedImage.DoesNotExist:
        out = 'Requested Image does not exist: {}, {}.{} ({})'.format(
            user_id,
            filename,
            extension,
            method
        )
        return jsonify(out), 404


@app.route("/api/user_metadata", methods=["POST"])
def handler_user_metadata():
    """
    Retrieve user data.
    """
    r = request.get_json()
    try:
        user_id = r['user_id']
        images = db.Image.objects.user(user_id)
        processimages = db.ProcessedImages.objects.user(user_id)
        filenames = [img.filename for img in images]
        extensions = [img.extension for img in images]
        proc_filenames = [img.filename for img in processimages]
        proc_times = [img.timeToProcess for img in processimages]
        processedAt = [img.processedAt for img in processimages]

        return_dict = {
            'filenames': filename,
            'extension': extensions,
            'proc_filenames': proc_filenames,
            'proc_times' = proc_times,
            'proc_processedAt' = processedAt
        }
        return jsonify(return_dict), 200
    except KeyError as e:
        errormessage = 'Field {} is missing.'.format(e)
        return jsonify(errormessage), 400
    except db.ProcessedImage.DoesNotExist:
        errormessage = 'User {} has no processed images.'.format(user_id)
        return jsonify(errormessage), 400


@app.route("/api/image_processing_metadata", methods=["POST"])
def handler_image_processing_metdata():
    """
    Retrieve data about image processing operations.
    """
    pass


if __name__ == '__main__':
    app.run()
