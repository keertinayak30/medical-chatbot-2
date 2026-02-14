# This is where you actually set your "SDK version" (Python version)
FROM python:3.10-slim

WORKDIR /app

# Standard Hugging Face user setup to avoid permission errors
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user . $HOME/app

RUN pip install --no-cache-dir -r requirements.txt

# Bind to 0.0.0.0 and port 7860
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]
