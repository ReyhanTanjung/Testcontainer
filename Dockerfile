# Menggunakan base image
FROM python:3.10

# Copy file ke dalam container
WORKDIR /app
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Tentukan perintah untuk menjalankan aplikasi
CMD ["python", "app/app.py"]
