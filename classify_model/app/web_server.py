from flask import Flask, request, jsonify, render_template
from model_server import get_label, get_tensor, get_model
import redis
import settings
from encode_image import prepare_image, base64_encode_image, base64_decode_image
import uuid
import time
from PIL import Image
import json
import io
import flask

app = Flask(__name__)

# Connect to redis server
db = redis.StrictRedis(host=settings.REDIS_HOST,
	port=settings.REDIS_PORT, db=settings.REDIS_DB)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def homepage():
    data = {"success": False}
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        if flask.request.files.get("image"):
            # read the image in PIL format and prepare it for
            # classification
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))
            image = prepare_image(image,
            (settings.IMAGE_WIDTH, settings.IMAGE_HEIGHT))

            # copy image and create due (id-image) to queue
            image = image.copy(order="C")
            image_id = str(uuid.uuid4())
            image = base64_encode_image(image)
            d = {"id": image_id, "image": image}
            db.rpush(settings.IMAGE_QUEUE, json.dumps(d))

            # loop for get output with id in db
            while True:
                # attempt to grab the output predictions
                output = db.get(image_id)
                if output is not None:
                    output = output.decode("utf-8")
                    data["predict"] = json.loads(output)
                    db.delete(image_id)
                    break
                time.sleep(settings.CLIENT_SLEEP)

            # indicate that the request was a success
            data["success"] = True
        else:
            return render_template('error.html')

    # return the data dictionary as a JSON response
    return render_template('predict.html', class_index_name=data['predict'][0])

@app.route("/about", methods=['GET'])
def about():
    if flask.request.method == 'GET':
        return render_template('about.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)