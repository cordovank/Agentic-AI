FROM python:3.13.5-slim

# Create user with ID 1000 (required for Hugging Face Spaces)
RUN useradd -m -u 1000 user
WORKDIR /app

# Install dependencies
COPY --chown=user requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY --chown=user . /app

# Switch to user and set environment
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Run Streamlit on port 7860
CMD ["streamlit", "run", "src/app.py", "--server.port=7860", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]