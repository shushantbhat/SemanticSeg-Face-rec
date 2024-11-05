from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import base64
import io

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    image = Image.open(file)

    # Process image (dummy example; replace with model processing)
    mask = image.convert("L")  # Placeholder for model mask generation

    # Convert mask image to base64 string
    buffered = io.BytesIO()
    mask.save(buffered, format="PNG")
    mask_base64 = base64.b64encode(buffered.getvalue()).decode()

    return jsonify({'mask': mask_base64})

if __name__ == '__main__':
    app.run(port=5173, debug=True)
