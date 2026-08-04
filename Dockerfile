FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Hugging Face Docker Spaces run the container as a non-root user (uid 1000).
# Create that user, pre-create every directory the app writes to at runtime
# (sqlite db, student photos, face embeddings, temp uploads), and hand
# ownership of the whole app directory to that user so writes don't fail
# with "Permission denied" once the container drops root.
RUN mkdir -p data/embeddings data/student_images data/temp_uploads data/test_images \
    && chmod +x start.sh \
    && useradd -m -u 1000 appuser \
    && chown -R appuser:appuser /app

USER appuser
ENV HOME=/home/appuser

# Hugging Face Docker Spaces route external traffic to port 7860
EXPOSE 7860

CMD ["./start.sh"]
