# Gunakan Python sebagai base image
FROM python:3.10-slim

# Atur direktori kerja di dalam container
WORKDIR /app

# Salin file proyek ke dalam container
COPY . /app

# Instal dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Jalankan aplikasi dengan Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
