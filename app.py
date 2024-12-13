from flask import Flask, request, jsonify
import pickle
import numpy as np
import tensorflow as tf

# Inisialisasi Flask
app = Flask(__name__)

# Load model dari file .pkl
model_path = 'model.pkl'
with open(model_path, 'rb') as pkl_file:
    model_data = pickle.load(pkl_file)

# Ambil variabel dari dictionary model
W = model_data['W'].numpy()  # Bobot
X = model_data['X'].numpy()  # Fitur
b = model_data['b'].numpy()  # Bias

# Endpoint untuk informasi model
@app.route('/model-info', methods=['GET'])
def model_info():
    info = {
        "weights_shape": W.shape,
        "features_shape": X.shape,
        "bias_shape": b.shape
    }
    return jsonify(info)

# Endpoint untuk prediksi
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Ambil data dari request
        input_data = request.get_json()
        input_features = np.array(input_data['features'])

        # Lakukan perhitungan prediksi
        # Prediksi = WX + b
        prediction = np.dot(W, input_features.T) + b
        prediction = prediction.flatten()  # Flatten array menjadi 1D

        # Cari indeks item dengan skor prediksi tertinggi
        top_indices = prediction.argsort()[-5:][::-1]  # Ambil 5 skor tertinggi
        top_scores = prediction[top_indices]  # Skor berdasarkan indeks

        # Format rekomendasi
        recommendations = [
            {"item_index": int(idx), "score": float(score)}
            for idx, score in zip(top_indices, top_scores)
        ]

        return jsonify({"recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Jalankan server
if __name__ == '__main__':
    app.run(debug=True)
