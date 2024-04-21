import os
from flask import Flask, request, jsonify
import requests
import pytesseract
from PIL import Image


app = Flask(__name__)


@app.route("/", methods=["POST"])
def ocr():
    rd = request.json
    img = rd.pop('image_url')
    f = requests.get(img, stream=True).raw
    s = pytesseract.image_to_string(Image.open(f))
    return jsonify({"result": s})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
