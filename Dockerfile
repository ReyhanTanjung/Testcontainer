# Menggunakan base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy semua file ke dalam container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Set environment variables untuk Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Tentukan perintah untuk menjalankan aplikasi
CMD ["flask", "run"]