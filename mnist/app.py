import base64
from fastapi import FastAPI, UploadFile, File
import tensorflow as tf
import numpy as np
from PIL import Image
import io

def preprocess_mnist(image: Image.Image):
    image = image.convert("L")

    # Resize while keeping aspect ratio
    image = image.resize((28, 28), Image.BILINEAR)

    img = np.array(image)

    # Invert
    img = 255 - img

    # Threshold (remove background noise)
    img = np.where(img > 50, img, 0)

    # Normalize
    img = img.astype("float32") / 255.0

    return img.reshape(1, 28, 28, 1),img


def image_to_base64(img_28x28: np.ndarray):
    img_uint8 = (img_28x28 * 255).astype(np.uint8)
    pil_img = Image.fromarray(img_uint8)

    buffer = io.BytesIO()
    pil_img.save(buffer, format="PNG")

    return base64.b64encode(buffer.getvalue()).decode("utf-8")



app = FastAPI(title="MNIST Digit Classifier API")

# Load model ONCE at startup
# Use ONE of the following depending on how you saved the model

# If saved as folder (recommended)
model = tf.keras.models.load_model("my_model.keras")

# If saved as file
# model = tf.keras.models.load_model("my_model.keras")

@app.get("/")
def health_check():
    return {"status": "MNIST API running", "tf_version": tf.__version__}

@app.post("/predict")
async def predict_digit(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    model_input, processed_img = preprocess_mnist(image)

    probs = model.predict(model_input, verbose=0)[0]

    predicted_digit = int(np.argmax(probs))
    confidence = float(np.max(probs))

    all_predictions = {
        str(i): float(probs[i]) for i in range(10)
    }

    processed_image_base64 = image_to_base64(processed_img)

    return {
        "predicted_digit": predicted_digit,
        "confidence": confidence,
        "all_predictions": all_predictions,
        "processed_image_base64": processed_image_base64
    }

