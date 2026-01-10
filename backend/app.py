from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from PIL import Image
import base64
import io

app = Flask(__name__)
CORS(app)

# 🔑 Put your OpenAI API key here
client = OpenAI(api_key="OPEN_API_KEY")




@app.route("/")
def home():
    return "Backend is running!"

def image_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")

@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image received"}), 400

    image_bytes = request.files["image"].read()
    image_b64 = image_to_base64(image_bytes)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image clearly for a visually impaired person."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        },
                    },
                ],
            }
        ],
    )

    description = response.choices[0].message.content
    return jsonify({"description": description})


if __name__ == "__main__":
    app.run(debug=True)
