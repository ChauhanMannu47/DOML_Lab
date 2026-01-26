# # Access & Test Frontend
# Run: uvicorn app:app --reload
# Open browser: http://localhost:8000/docs
# Click POST /predict/ > Try it out
# Choose file > Select your ZIP of 100 PNGs
# Click Execute

# Recmmended : pip install fastapi uvicorn joblib pillow numpy scikit-learn

# pip list | findstr "fastapi uvicorn joblib pillow numpy scikit-learn"
# fastapi           0.128.0
# joblib            1.5.3
# numpy             2.4.1
# pillow            12.1.0
# scikit-learn      1.8.0
# uvicorn           0.40.0


from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import joblib
import numpy as np
from PIL import Image
from io import BytesIO
import zipfile
import os
import shutil

app = FastAPI(title="MNIST Predictor API")

# Load model FIRST (LinearSVC), then metadata
try:
    model = joblib.load("mnist_linear_svc.pkl")  # Your SVM model
    metadata = joblib.load("mnist_metadata.pkl")  # Optional metadata
    print("Model and metadata loaded successfully!")
except FileNotFoundError as e:
    print(f"Missing file: {e}. Place both .pkl files in the same folder as app.py")
    raise

@app.post("/predict/")
async def predict_from_zip(zip_file: UploadFile = File(...)):
    if not zip_file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Upload must be a ZIP file")
    
    temp_dir = "temp_images"
    os.makedirs(temp_dir, exist_ok=True)
    predictions = []
    try:
        zip_content = await zip_file.read()
        with zipfile.ZipFile(BytesIO(zip_content)) as z:
            z.extractall(temp_dir)
        
        for file in os.listdir(temp_dir):
            if file.lower().endswith('.png'):
                img_path = os.path.join(temp_dir, file)
                img = Image.open(img_path).convert('L')
                img = img.resize((28, 28), Image.Resampling.LANCZOS)  # Fix size automatically
                
                img_array = np.array(img).flatten().reshape(1, -1) / 255.0
                pred = model.predict(img_array)[0]
                predictions.append({"filename": file, "prediction": int(pred)})

        
        if len(predictions) == 0:
            raise HTTPException(status_code=400, detail="No PNG images found in ZIP")
        
        return JSONResponse(content={"predictions": predictions})
    
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


