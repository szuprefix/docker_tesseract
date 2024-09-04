import os
import requests
from PIL import Image

from flask import Flask, request, jsonify
DEBUG = os.environ.get('DEBUG', False)

app = Flask(__name__)
import logs


@app.route("/", methods=["POST"])
def ocr():
    import pytesseract
    if 'file' in request.files:
        f = request.files['file']
    else:
        rd = request.json
        img = rd.pop('image_url')
        f = requests.get(img, stream=True).raw
    s = pytesseract.image_to_string(Image.open(f))
    return jsonify({"result": s})


@app.route("/error", methods=["GET"])
def error():
    # app.logger.error('test')
    a = 3 / 0
    return 'hello'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)
