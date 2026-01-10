from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image received"}), 400

    image = request.files["image"]
    return jsonify({
        "message": "Image received successfully",
        "filename": image.filename
    })

if __name__ == "__main__":
    app.run(debug=True)
