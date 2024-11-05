from flask import Flask, jsonify
import cv2
import numpy as np
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image

app = Flask(__name__)

# Initialize MTCNN for face detection and InceptionResnetV1 for embeddings
mtcnn = MTCNN(keep_all=True, device='cuda' if torch.cuda.is_available() else 'cpu')
resnet = InceptionResnetV1(pretrained='casia-webface').eval()

# Known face encodings
known_face_encodings = []
known_face_names = []

# Function to load and encode known faces
def load_known_faces():
    image_path = r"C:\Users\shush\OneDrive\Pictures\Camera Roll\WIN_20241105_16_35_25_Pro.jpg"
    encoding, _ = get_face_embeddings(Image.open(image_path))
    if encoding is not None:
        known_face_encodings.append(encoding[0])  # first embedding
        known_face_names.append("Shushant Bhat")

def get_face_embeddings(pil_image):
    boxes, _ = mtcnn.detect(pil_image)
    if boxes is not None:
        aligned = mtcnn(pil_image)
        embeddings = resnet(aligned).detach()
        return embeddings, boxes
    return None, None

load_known_faces()

# Route for face recognition
@app.route('/face-recognition', methods=['GET'])
def recognize_face():
    cap = cv2.VideoCapture(0)
    recognized = False

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        embeddings, boxes = get_face_embeddings(img)

        if boxes is not None:
            for i, box in enumerate(boxes):
                face_embedding = embeddings[i]
                distances = [
                    torch.nn.functional.pairwise_distance(face_embedding.unsqueeze(0), encoding.unsqueeze(0)).item()
                    for encoding in known_face_encodings
                ]
                if min(distances) < 0.6:
                    recognized = True
                    break

        if recognized:
            break

    cap.release()
    cv2.destroyAllWindows()

    return jsonify({"status": "recognized" if recognized else "not recognized"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
